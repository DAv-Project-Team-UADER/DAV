"""Single shared microphone + Vosk engine for DAV (CAD navigation and preferences)."""

from __future__ import annotations

import json
import queue
import threading
import time
from dataclasses import dataclass
from typing import Callable, Literal

from core.dav_log import get_logger
from core.model_manager import get_active_model_path, has_small_model
from core.settings import settings
from speech.voice_commands import _buffer_to_bytes, match_command

log = get_logger("voz")

VoiceMode = Literal["idle", "cad", "preferences"]


@dataclass
class _PreferencesCallbacks:
    on_command: Callable[[str], None]
    on_text: Callable[[str, bool], None] | None
    on_status: Callable[[str], None] | None
    on_audio: Callable[[], None] | None
    language: str


class DavVoiceService:
    """One mic thread; routes recognition to CAD or preferences handlers."""

    _instance: DavVoiceService | None = None

    @classmethod
    def get(cls) -> DavVoiceService:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._mode: VoiceMode = "idle"
        self._cad_adapter = None
        self._prefs: _PreferencesCallbacks | None = None
        self._prefs_enabled = True
        self._cad_active_before_prefs = False
        self._thread: threading.Thread | None = None
        self._stop_event = threading.Event()
        self._running = False
        self._mic_open = False
        self._accept_callbacks = False
        self._language = "es"
        self._model_size = "small"
        self._last_prefs_cmd: str | None = None
        self._last_prefs_cmd_time = 0.0
        self._grammar_queue: queue.Queue[str] = queue.Queue()

    def set_grammar(self, phrases: list[str] | None) -> None:
        """Dynamically update recognizer grammar with a list of valid spoken phrases."""
        if phrases is None:
            return
        phrases_list = [p.lower().strip() for p in phrases if p]
        if "[unk]" not in phrases_list:
            phrases_list.append("[unk]")
        grammar_json = json.dumps(phrases_list, ensure_ascii=False)
        self._grammar_queue.put(grammar_json)

    # --- Public API ---

    def is_mic_running(self) -> bool:
        return self._running and self._mic_open

    def is_mic_starting(self) -> bool:
        return self._running and not self._mic_open

    def is_cad_active(self) -> bool:
        with self._lock:
            return self._mode == "cad" and self._running

    def is_preferences_active(self) -> bool:
        with self._lock:
            return self._mode == "preferences" and self._prefs is not None

    def is_cad_engine_loaded(self) -> bool:
        with self._lock:
            return self._cad_adapter is not None

    def start_cad(self, cad_adapter) -> bool:
        settings.load()
        with self._lock:
            if self._mode == "cad" and self._running:
                return True
            self._cad_adapter = cad_adapter
            self._mode = "cad"
        browser = getattr(cad_adapter, "_browser", getattr(cad_adapter, "browser", None))
        if browser is not None and hasattr(browser, "GetSpokenPhrases"):
            self.set_grammar(browser.GetSpokenPhrases())
        return self._ensure_mic(settings.language, settings.model_size)

    def attach_preferences(
        self,
        language: str,
        *,
        on_command: Callable[[str], None],
        on_text: Callable[[str, bool], None] | None = None,
        on_status: Callable[[str], None] | None = None,
        on_audio: Callable[[], None] | None = None,
    ) -> bool:
        with self._lock:
            # Keep CAD alive whenever the CAD engine was started before prefs.
            self._cad_active_before_prefs = self._cad_adapter is not None
            self._prefs = _PreferencesCallbacks(
                on_command=on_command,
                on_text=on_text,
                on_status=on_status,
                on_audio=on_audio,
                language=language,
            )
            self._prefs_enabled = True
            self._mode = "preferences"
            self._last_prefs_cmd = None
            self._last_prefs_cmd_time = 0.0
        try:
            from speech.voice_commands import all_grammar_phrases

            self.set_grammar(all_grammar_phrases())
        except Exception:
            # Sin gramatica el reconocimiento sigue andando, pero contra el
            # vocabulario entero del modelo: hay que enterarse, no tragarlo.
            log.exception("no se pudo armar la gramatica de preferencias")
        return self._ensure_mic(language, settings.model_size)

    def detach_preferences(self) -> None:
        with self._lock:
            self._prefs = None
            restore_cad = self._cad_adapter is not None
            if restore_cad:
                self._mode = "cad"
            else:
                self._mode = "idle"
            self._cad_active_before_prefs = False
        if restore_cad:
            self.resume_cad_voice()
            return
        self.stop(wait=False)

    def resume_cad_voice(self) -> None:
        """Return to CAD routing after preferences (keep the same mic thread)."""
        adapter = None
        with self._lock:
            if self._cad_adapter is None:
                return
            self._mode = "cad"
            self._prefs = None
            self._prefs_enabled = True
            self._cad_active_before_prefs = False
            adapter = self._cad_adapter
            language = self._language
            model_size = self._model_size
        adapter._stop_requested = False
        self._stop_event.clear()
        browser = getattr(adapter, "_browser", getattr(adapter, "browser", None))
        if browser is not None and hasattr(browser, "GetSpokenPhrases"):
            self.set_grammar(browser.GetSpokenPhrases())
        if self._running and self._thread and self._thread.is_alive():
            self._accept_callbacks = True
            return
        self._ensure_mic(language, model_size)

    def set_preferences_listening(self, enabled: bool) -> None:
        with self._lock:
            self._prefs_enabled = enabled
            if self._mode != "preferences":
                return
            prefs = self._prefs
        if enabled and prefs and not self._running:
            self._ensure_mic(prefs.language, settings.model_size)
        elif not enabled and self._cad_adapter is None:
            self.stop(wait=False)

    def preferences_listening(self) -> bool:
        with self._lock:
            return (
                self._mode == "preferences"
                and self._prefs_enabled
                and self._running
                and self._mic_open
            )

    def preferences_starting(self) -> bool:
        with self._lock:
            return (
                self._mode == "preferences"
                and self._prefs_enabled
                and self._running
                and not self._mic_open
            )

    def stop(self, *, wait: bool = True, timeout: float = 4.0) -> None:
        adapter = None
        with self._lock:
            self._mode = "idle"
            self._prefs = None
            self._cad_active_before_prefs = False
            adapter = self._cad_adapter
            self._cad_adapter = None
        if adapter is not None:
            adapter.request_stop()
        self._accept_callbacks = False
        self._stop_event.set()
        self._mic_open = False
        if wait and self._thread and self._thread.is_alive():
            self._thread.join(timeout=timeout)
        self._running = False
        self._thread = None

    def request_cad_stop(self) -> None:
        with self._lock:
            if self._cad_adapter is not None:
                self._cad_adapter.request_stop()

    # --- Mic thread ---

    def _ensure_mic(self, language: str, model_size: str) -> bool:
        need_restart = self._running and (
            language != self._language or model_size != self._model_size
        )
        if need_restart:
            log.info(
                "reiniciando mic: %s/%s -> %s/%s",
                self._language,
                self._model_size,
                language,
                model_size,
            )
            self._accept_callbacks = False
            self._stop_event.set()
            if self._thread and self._thread.is_alive():
                self._thread.join(timeout=3.0)
            self._running = False
            self._thread = None
            self._stop_event.clear()

        self._language = language
        self._model_size = model_size
        if not has_small_model(language) and model_size == "small":
            self._emit_prefs_status("error:no_model")
            return False
        model_path = get_active_model_path(language, model_size)
        if model_path is None:
            self._emit_prefs_status("error:no_model")
            return False
        if self._running and self._thread and self._thread.is_alive():
            self._emit_prefs_status("active")
            return True
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._listen_loop,
            args=(str(model_path),),
            name="DAV-VoiceService",
            daemon=True,
        )
        self._thread.start()
        self._running = True
        return True

    def _safe_call(self, callback: Callable | None, *args) -> None:
        if not callback or not self._accept_callbacks:
            return
        try:
            callback(*args)
        except RuntimeError:
            pass
        except Exception:
            pass

    def _emit_prefs_status(self, message: str) -> None:
        with self._lock:
            prefs = self._prefs
        if prefs and prefs.on_status:
            self._safe_call(prefs.on_status, message)

    def _listen_loop(self, model_path: str) -> None:
        log.info("hilo de voz arrancando: modelo=%s", model_path)
        try:
            import sounddevice as sd
            from vosk import KaldiRecognizer, Model
        except ImportError as exc:
            log.exception("faltan dependencias de voz (sounddevice/vosk)")
            self._emit_prefs_status(f"error:import:{exc}")
            self._running = False
            return

        sample_rate = 16000
        try:
            model = Model(model_path)
            recognizer = KaldiRecognizer(model, sample_rate)
        except Exception as exc:
            log.exception("no se pudo cargar el modelo Vosk: %s", model_path)
            self._emit_prefs_status(f"error:model:{exc}")
            self._running = False
            return
        log.info("modelo cargado, recognizer listo")

        audio_q: queue.Queue[bytes] = queue.Queue()
        last_text = ""

        def callback(indata, frames, time_info, status) -> None:
            if not self._accept_callbacks or self._stop_event.is_set():
                return
            try:
                audio_q.put(_buffer_to_bytes(indata), block=False)
            except Exception:
                return
            with self._lock:
                prefs = self._prefs
            if prefs and prefs.on_audio and self._mode == "preferences" and self._prefs_enabled:
                self._safe_call(prefs.on_audio)

        stream = None
        try:
            stream = sd.RawInputStream(
                samplerate=sample_rate,
                blocksize=4000,
                dtype="int16",
                channels=1,
                callback=callback,
            )
            self._accept_callbacks = True
            with stream:
                self._mic_open = True
                self._emit_prefs_status("active")
                while not self._stop_event.is_set():
                    while not self._grammar_queue.empty():
                        try:
                            g_json = self._grammar_queue.get_nowait()
                            if g_json:
                                # Vosk aborta el proceso si se le cambia la
                                # gramatica a un recognizer que ya proceso audio:
                                #   SetGrm():recognizer.cc:235
                                #   "Can't add speaker model to already running
                                #    recognizer"
                                # No es una excepcion de Python: se lleva FreeCAD
                                # entero (ver crash.log, Recognizer::SetGrm).
                                # Reset() lo devuelve a estado inicial y ahi si
                                # acepta la gramatica nueva. Verificado contra el
                                # modelo pt, que era el que crasheaba.
                                log.info(
                                    "aplicando gramatica: %d frases",
                                    g_json.count(",") + 1,
                                )
                                recognizer.Reset()
                                recognizer.SetGrammar(g_json)
                                log.info("gramatica aplicada")
                        except queue.Empty:
                            break
                        except Exception as exc:
                            log.exception("fallo SetGrammar")
                            print(f"[DavVoiceService] Error setting grammar: {exc}")

                    try:
                        data = audio_q.get(timeout=0.5)
                    except queue.Empty:
                        continue
                    if recognizer.AcceptWaveform(data):
                        result = json.loads(recognizer.Result())
                        self._dispatch_text(result.get("text", ""), final=True)
                    else:
                        partial = json.loads(recognizer.PartialResult())
                        self._dispatch_text(partial.get("partial", ""), final=False)
        except Exception as exc:
            log.exception("el loop de audio murio")
            self._emit_prefs_status(f"error:mic:{exc}")
        finally:
            # Si el log termina aca sin "hilo de voz terminado", el proceso se
            # cayo dentro del loop: mirar crash.log de FreeCAD.
            log.info(
                "hilo de voz terminado (stop_event=%s)", self._stop_event.is_set()
            )
            self._accept_callbacks = False
            self._mic_open = False
            self._running = False
            if stream is not None:
                try:
                    stream.stop()
                    stream.close()
                except Exception:
                    pass

    def _dispatch_text(self, text: str, *, final: bool) -> None:
        text = text.strip()
        if not text:
            return
        with self._lock:
            mode = self._mode
            prefs = self._prefs
            prefs_enabled = self._prefs_enabled
            cad_adapter = self._cad_adapter

        if mode == "preferences" and prefs and prefs_enabled:
            self._handle_preferences_text(text, final, prefs)
            return
        if mode == "cad":
            if self._dispatch_to_active_prompt(text, final=final):
                return
            if final and cad_adapter is not None:
                log.info("cad: frase reconocida %r", text)
                cad_adapter.procesar_frase_final(text)

    def _dispatch_to_active_prompt(self, text: str, *, final: bool) -> bool:
        try:
            from InputPrompts.PromptVoiceRouter import PromptVoiceRouter

            return PromptVoiceRouter.ProcessVoiceText(text, Final=final)
        except ImportError:
            # InputPrompts no montado: es el caso normal, no se loguea.
            return False
        except Exception:
            # pendientes-dav.md 9.c: este except se tragaba los fallos de
            # InputPrompts sin dejar rastro. Sigue sin interrumpir la voz,
            # pero ahora queda registrado.
            log.exception("PromptVoiceRouter fallo con %r", text)
            return False

    def _handle_preferences_text(self, text: str, final: bool, prefs: _PreferencesCallbacks) -> None:
        if prefs.on_text:
            self._safe_call(prefs.on_text, text, final)
        if not final:
            return
        cmd = match_command(text)
        if not cmd:
            log.debug("preferencias: sin match para %r", text)
            self._safe_call(prefs.on_status, f"unknown:{text}")
            return
        # Deja registro de que frase disparo cada comando: es la unica forma de
        # rastrear los cambios de idioma que el usuario no pidio.
        log.info("preferencias: %r -> %s", text, cmd)
        now = time.monotonic()
        if cmd == self._last_prefs_cmd and (now - self._last_prefs_cmd_time) < 1.5:
            return
        self._last_prefs_cmd = cmd
        self._last_prefs_cmd_time = now
        self._safe_call(prefs.on_command, cmd)

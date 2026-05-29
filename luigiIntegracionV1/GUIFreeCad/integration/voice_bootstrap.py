"""Start/stop unified DAV voice from GUIFreeCad (no changes to PruebaIntegracion core)."""

from __future__ import annotations

import traceback

from integration.dav_paths import ensure_dav_repo_on_path, ensure_gui_on_path
from speech.dav_voice_service import DavVoiceService


def is_voice_running() -> bool:
    return DavVoiceService.get().is_cad_engine_loaded()


def start_voice_engine(*, debug: bool = False) -> bool:
    try:
        ensure_gui_on_path()
        ensure_dav_repo_on_path()
        from core.model_manager import get_active_model_path
        from core.settings import settings

        settings.load()
        model = get_active_model_path(settings.language, settings.model_size)
        if model is None:
            _print_error(
                "[DAV] Sin modelo Vosk para idioma "
                f"'{settings.language}'. Configurá Preferencias DAV o ejecutá "
                "python scripts/setup_models.py en GUIFreeCad.\n"
            )
            return False

        svc = DavVoiceService.get()
        if svc.is_cad_engine_loaded():
            _print_message("[DAV] El motor de voz ya está activo.\n")
            return True

        from core.language_code import LanguageCode
        from core.preferences import preferences
        from integration.cad_session import build_explorador_voz
        from integration.cad_voice_adapter import CadStreamingAdapter

        preferences.SetLanguage = LanguageCode.FromStorage(settings.language)

        # TODO Developer 4: replace CadStreamingAdapter with BrowserVoiceAdapter
        # once the Browser search engine (Developer 3) is implemented.
        # Example:
        #   from integration.browser_voice_adapter import BrowserVoiceAdapter
        #   adapter = BrowserVoiceAdapter()
        explorador = build_explorador_voz(model, settings.language, debug=debug)
        adapter = CadStreamingAdapter(explorador)
        if not svc.start_cad(adapter):
            return False

        _print_message(
            "[DAV] Voz activa (motor unificado). Ejemplos: «preferencias enviar», "
            "«archivo enviar» → «nuevo enviar».\n"
        )
        return True
    except Exception:
        _print_error("[DAV] No se pudo iniciar la voz:\n")
        _print_error(traceback.format_exc())
        return False


def stop_voice_engine(*, wait: bool = True, timeout: float = 4.0) -> None:
    svc = DavVoiceService.get()
    if not svc.is_cad_engine_loaded() and not svc.is_mic_running():
        _print_message("[DAV] El motor de voz no está activo.\n")
        return
    _print_message("[DAV] Deteniendo voz… (puede tardar un instante).\n")
    svc.stop(wait=wait, timeout=timeout)
    _print_message("[DAV] Motor de voz detenido.\n")


def _print_message(text: str) -> None:
    try:
        import FreeCAD as App

        App.Console.PrintMessage(text)
    except ImportError:
        print(text, end="")


def _print_error(text: str) -> None:
    try:
        import FreeCAD as App

        App.Console.PrintError(text)
    except ImportError:
        print(text, end="", file=__import__("sys").stderr)

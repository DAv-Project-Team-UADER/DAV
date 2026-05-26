"""Voice command listener using Vosk small model."""

from __future__ import annotations

import re
import unicodedata
from typing import Callable

from core.model_manager import has_small_model

# SetGrammar can block all recognition on some models — leave False to debug
USE_GRAMMAR = False


def _buffer_to_bytes(indata) -> bytes:
    """Convert sounddevice/cffi audio buffer to bytes (safe across versions)."""
    if isinstance(indata, (bytes, bytearray)):
        return bytes(indata)
    if hasattr(indata, "tobytes"):
        return indata.tobytes()
    return bytes(memoryview(indata))

# Phrases mapped to internal command ids (multi-language)
COMMAND_MAP: dict[str, list[str]] = {
    "lang_en": [
        "english", "inglés", "ingles", "inglês", "inglesh",
    ],
    "lang_es": [
        "spanish", "español", "espanol", "espanhol", "castellano",
    ],
    "lang_pt": [
        "portuguese", "portugués", "portugues", "português", "portuguesa",
        "brasil", "brazil", "idioma portugues", "idioma português",
    ],
    "model_small": [
        "small model", "modelo pequeño", "modelo pequeno",
        "pequeño modelo", "modelo chico", "modelo menor",
    ],
    "model_large": [
        "large model", "modelo grande", "modelo largo", "grande modelo",
    ],
    "theme_light": [
        "light theme", "tema claro", "claro", "light", "blanco", "tema blanco",
    ],
    "theme_dark": [
        "dark theme", "tema oscuro", "oscuro", "dark", "negro", "tema negro",
    ],
    "startup_on": [
        "startup on", "arranque activado", "inicialização ativada", "activado", "ativado",
    ],
    "startup_off": [
        "startup off", "arranque desactivado", "arranque desactivado",
        "inicialização desativada", "desactivado", "desativado",
    ],
    "yes": ["yes", "sí", "si", "sim", "yeah", "confirmar", "confirmar sim", "quero sim"],
    "no": ["no", "não", "nao", "nop", "negativo", "cancelar", "nao quero", "não quero"],
    "apply": ["apply", "aplicar", "aplicar"],
    "ok": ["ok", "aceptar", "accept", "confirmar"],
    "open_preferences": [
        "preferencias", "abrir preferencias", "open preferences",
        "configuracion", "configuración", "ajustes", "opciones",
        "settings", "preferences",
    ],
}

def _normalize(text: str) -> str:
    """Lowercase and strip accents for fuzzy matching."""
    text = text.lower().strip()
    return "".join(
        c
        for c in unicodedata.normalize("NFD", text)
        if unicodedata.category(c) != "Mn"
    )


# Longest phrases first so "modelo pequeño" wins over "pequeño"
_PHRASES_SORTED: list[tuple[str, str]] = []
for cmd_id, phrases in COMMAND_MAP.items():
    for phrase in phrases:
        _PHRASES_SORTED.append((_normalize(phrase), cmd_id))
_PHRASES_SORTED.sort(key=lambda x: len(x[0]), reverse=True)


def _contains_phrase(normalized: str, phrase: str) -> bool:
    """Frases cortas solo como palabra completa (evita falsos positivos en PT)."""
    if normalized == phrase:
        return True
    if len(phrase) <= 4:
        return bool(re.search(r"(?:^|\s)" + re.escape(phrase) + r"(?:\s|$)", normalized))
    return phrase in normalized


def all_grammar_phrases() -> list[str]:
    """All phrases for Vosk constrained grammar."""
    seen: set[str] = set()
    out: list[str] = []
    for phrases in COMMAND_MAP.values():
        for phrase in phrases:
            key = phrase.lower().strip()
            if key not in seen:
                seen.add(key)
                out.append(key)
    return out


def match_command(text: str) -> str | None:
    if not text or not text.strip():
        return None
    normalized = _normalize(text)
    for phrase, cmd_id in _PHRASES_SORTED:
        if _contains_phrase(normalized, phrase):
            return cmd_id
    return None


class VoiceCommandListener:
    """Preferences voice — uses the shared DavVoiceService (same mic as CAD)."""

    def __init__(
        self,
        language: str,
        on_command: Callable[[str], None],
        on_text: Callable[[str, bool], None] | None = None,
        on_status: Callable[[str], None] | None = None,
        on_audio: Callable[[], None] | None = None,
        sample_rate: int = 16000,
    ) -> None:
        self._language = language
        self._on_command = on_command
        self._on_text = on_text
        self._on_status = on_status
        self._on_audio = on_audio
        self._sample_rate = sample_rate  # kept for API compatibility
        from speech.dav_voice_service import DavVoiceService

        self._service = DavVoiceService.get()
        self._attached = False

    def is_running(self) -> bool:
        return self._service.preferences_listening()

    def is_starting(self) -> bool:
        return self._service.preferences_starting()

    def start(self) -> bool:
        if not has_small_model(self._language):
            if self._on_status:
                try:
                    self._on_status("error:no_model")
                except RuntimeError:
                    pass
            return False
        ok = self._service.attach_preferences(
            self._language,
            on_command=self._on_command,
            on_text=self._on_text,
            on_status=self._on_status,
            on_audio=self._on_audio,
        )
        self._attached = ok
        return ok

    def pause(self) -> None:
        self._service.set_preferences_listening(False)

    def resume(self) -> bool:
        self._service.set_preferences_listening(True)
        return self.is_running() or self.is_starting()

    def stop(self, wait: bool = True, timeout: float = 2.0) -> None:
        if self._attached:
            self._service.detach_preferences()
            self._attached = False
        else:
            self._service.set_preferences_listening(False)
        # wait/timeout kept for API compatibility; detach is non-blocking when CAD resumes


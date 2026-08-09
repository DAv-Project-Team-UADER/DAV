"""
BrowserVoiceAdapter: connects Vosk spoken phrases to the new Browser navigation engine.
"""

from __future__ import annotations

import unicodedata
from typing import Any

from navigation.browser import Browser
from integration.voice_history import append_voice_history, export_context_state


def _normalize(text: str) -> str:
    decomposed = unicodedata.normalize("NFKD", text)
    stripped = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return " ".join(stripped.lower().split())


_SEND_WORDS = {"enviar", "send"}
_CANCEL_WORDS = {"cancelar", "cancel"}


class BrowserVoiceAdapter:
    """Adapter to feed the raw phrase directly to the Browser's ProcessPhrase."""

    def __init__(self, browser: Browser) -> None:
        self._browser = browser
        self._stop_requested = False

    @property
    def explorador(self) -> Any:
        return None

    def request_stop(self) -> None:
        self._stop_requested = True

    def procesar_frase_final(self, raw_phrase: str) -> None:
        if self._stop_requested or not raw_phrase:
            return

        normalized = _normalize(raw_phrase)
        print(f"[BrowserVoiceAdapter] Received phrase: '{raw_phrase}'")
        append_voice_history(f"[DAV] Voz: {raw_phrase}")

        token = self._extract_token(normalized)
        if token is None:
            return
        if token is False:
            print("[DAV Browser] Cancelled.")
            return

        # Acciones que cambian de nivel: tras ellas mostramos el contexto.
        _NAV_ACTIONS = {"descend", "back", "base_jump"}

        def _run() -> None:
            result = self._browser.ProcessPhrase(token)
            if result.Success:
                print(f"[DAV Browser] Success ({result.Action}): {result.Message}")
                append_voice_history(f"[DAV] OK ({result.Action}): {result.Message}")
                if result.Action in _NAV_ACTIONS:
                    print(self._browser.DescribeContext())
                    append_voice_history(self._browser.DescribeContext())
            else:
                print(f"[DAV Browser] Ignored: {result.Message}")
                append_voice_history(f"[DAV] Ignorado: {result.Message}")
            self._export_state()

        try:
            from integration.freecad_gui_bridge import run_on_main_thread
            run_on_main_thread(_run)
        except ImportError:
            _run()

    def _export_state(self) -> None:
        submenus = []
        commands = []
        seen_targets = []
        for entry in self._browser.Context:
            if any(self._browser._SameTarget(entry.Target, t) for t in seen_targets):
                continue
            seen_targets.append(entry.Target)
            item = {"spoken": entry.Spoken, "key": entry.InternalKey}
            if entry.IsSubContext():
                submenus.append(item)
            elif entry.IsCallable():
                commands.append(item)
                
        state = {
            "context_path": self._browser.ContextPath,
            "submenus": submenus,
            "commands": commands
        }
        export_context_state(state)

    @staticmethod
    def _extract_token(normalized: str):
        """Return command token, False for cancel, None to ignore."""
        for word in _CANCEL_WORDS:
            if normalized == word or normalized.endswith(" " + word):
                return False
        for word in _SEND_WORDS:
            if normalized.endswith(" " + word):
                token = normalized[: -(len(word) + 1)].strip()
                return token or None
            if normalized == word:
                return None
        return normalized or None

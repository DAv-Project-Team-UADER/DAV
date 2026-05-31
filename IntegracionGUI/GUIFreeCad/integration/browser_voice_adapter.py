"""
BrowserVoiceAdapter: connects Vosk spoken phrases to the new Browser navigation engine.
"""

from __future__ import annotations
from typing import Any
from navigation.browser import Browser

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
        if self._stop_requested:
            return

        print(f"[BrowserVoiceAdapter] Received phrase: '{raw_phrase}'")
        result = self._browser.ProcessPhrase(raw_phrase)

        if result.Success:
            print(f"[DAV Browser] Success ({result.Action}): {result.Message}")
        else:
            print(f"[DAV Browser] Ignored: {result.Message}")

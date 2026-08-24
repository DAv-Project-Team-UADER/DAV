#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Route shared DAV voice recognition to the currently active input prompt."""

from __future__ import annotations

import threading
from typing import Any


def _IsNumericPrompt(Prompt: Any) -> bool:
    """Return True when the prompt requires numeric voice input."""
    if Prompt is None:
        return False
    try:
        from InputPrompts.IntegerInputPrompt import IntegerInputPrompt
        from InputPrompts.FloatInputPrompt import FloatInputPrompt
        return isinstance(Prompt, (IntegerInputPrompt, FloatInputPrompt))
    except ImportError:
        return False


class PromptVoiceRouter:
    """Thread-safe registry for the prompt currently collecting voice input."""

    _Lock = threading.RLock()
    _ActivePrompt: Any | None = None

    @classmethod
    def SetActivePrompt(cls, Prompt: Any) -> None:
        """Register a prompt as the active voice input target.

        When the prompt is numeric (Integer/Float), the Vosk grammar is
        switched to include number words so the recognizer can hear digits
        and decimal separators.
        """
        with cls._Lock:
            cls._ActivePrompt = Prompt
        if _IsNumericPrompt(Prompt):
            cls._ActivateNumericGrammar()

    @classmethod
    def ClearActivePrompt(cls, Prompt: Any | None = None) -> None:
        """Clear the active prompt, optionally only if it matches Prompt.

        When the cleared prompt was numeric, the Vosk grammar is restored
        to the CAD navigation context.
        """
        was_numeric = False
        with cls._Lock:
            if Prompt is None or cls._ActivePrompt is Prompt:
                was_numeric = _IsNumericPrompt(cls._ActivePrompt)
                cls._ActivePrompt = None
        if was_numeric:
            cls._RestoreCadGrammar()

    @classmethod
    def HasActivePrompt(cls) -> bool:
        """Return True when a prompt is currently collecting voice input."""
        with cls._Lock:
            return cls._ActivePrompt is not None

    @classmethod
    def ProcessVoiceText(cls, Text: str, *, Final: bool) -> bool:
        """Route recognized text to the active prompt.

        Returns True when a prompt consumed the text and CAD command routing
        should stop for this phrase.
        """
        with cls._Lock:
            prompt = cls._ActivePrompt

        if prompt is None:
            return False

        def _run() -> None:
            if Final:
                prompt.ProcessFinalText(Text)
            else:
                prompt.ProcessPartialText(Text)

        cls._RunOnMainThread(_run)
        return True

    @classmethod
    def _ActivateNumericGrammar(cls) -> None:
        """Switch Vosk grammar to include number words for numeric input."""
        try:
            import sys
            from pathlib import Path
            from speech.dav_voice_service import DavVoiceService
            from integration.voice_bootstrap import _resolve_dictionary_root

            dic_root = str(_resolve_dictionary_root())
            if dic_root not in sys.path:
                sys.path.insert(0, dic_root)

            from Numbers.Numbers import get_numeric_grammar_phrases
            phrases = get_numeric_grammar_phrases()
            DavVoiceService.get().set_grammar(phrases)
        except Exception:
            pass

    @classmethod
    def _RestoreCadGrammar(cls) -> None:
        """Restore the CAD navigation grammar after numeric input."""
        try:
            from speech.dav_voice_service import DavVoiceService
            from integration.browser_voice_adapter import _ActiveAdapter
            if _ActiveAdapter is not None:
                browser = _ActiveAdapter._browser
                if browser is not None and hasattr(browser, "GetSpokenPhrases"):
                    phrases = browser.GetSpokenPhrases()
                    DavVoiceService.get().set_grammar(phrases)
        except Exception:
            pass

    @staticmethod
    def _RunOnMainThread(Function) -> None:
        try:
            from integration.freecad_gui_bridge import run_on_main_thread

            run_on_main_thread(Function)
        except Exception:
            Function()

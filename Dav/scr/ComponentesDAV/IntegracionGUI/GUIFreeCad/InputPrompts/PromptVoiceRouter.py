#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Route shared DAV voice recognition to the currently active input prompt."""

from __future__ import annotations

import threading
from typing import Any

from InputPrompts.NumericGrammarSwitcher import NumericGrammarSwitcher
from InputPrompts.ObjectNameGrammarSwitcher import ObjectNameGrammarSwitcher
from InputPrompts.NewObjectNameGrammarSwitcher import NewObjectNameGrammarSwitcher


def _RequiresNumericGrammar(Prompt: Any) -> bool:
    """Return True when the prompt needs the numeric Vosk grammar.

    Delegates to the prompt itself (BaseInputPrompt.RequiresNumericGrammar)
    instead of checking concrete types, so a new numeric prompt class does
    not require changes here.
    """
    if Prompt is None:
        return False
    return bool(getattr(Prompt, "RequiresNumericGrammar", lambda: False)())


def _RequiresObjectNameGrammar(Prompt: Any) -> bool:
    """Return True when the prompt needs the object-label Vosk grammar.

    Same polymorphic approach as _RequiresNumericGrammar: the prompt declares
    its own grammar need, so adding a prompt type needs no change here.
    """
    if Prompt is None:
        return False
    return bool(getattr(Prompt, "RequiresObjectNameGrammar", lambda: False)())


def _RequiresNewObjectNameGrammar(Prompt: Any) -> bool:
    """Return True when the prompt needs the new-object-name vocabulary."""
    if Prompt is None:
        return False
    return bool(getattr(Prompt, "RequiresNewObjectNameGrammar", lambda: False)())


class PromptVoiceRouter:
    """Thread-safe registry for the prompt currently collecting voice input."""

    _Lock = threading.RLock()
    _ActivePrompt: Any | None = None

    @classmethod
    def SetActivePrompt(cls, Prompt: Any) -> None:
        """Register a prompt as the active voice input target.

        When the prompt requires numeric grammar, the Vosk grammar is
        switched to include number words so the recognizer can hear digits
        and decimal separators.
        """
        with cls._Lock:
            cls._ActivePrompt = Prompt
        if _RequiresNumericGrammar(Prompt):
            NumericGrammarSwitcher.ActivateNumericGrammar()
        elif _RequiresObjectNameGrammar(Prompt):
            ObjectNameGrammarSwitcher.ActivateObjectNameGrammar()
        elif _RequiresNewObjectNameGrammar(Prompt):
            NewObjectNameGrammarSwitcher.ActivateNewObjectNameGrammar()

    @classmethod
    def ClearActivePrompt(cls, Prompt: Any | None = None) -> None:
        """Clear the active prompt, optionally only if it matches Prompt.

        When the cleared prompt required numeric grammar, the Vosk grammar
        is restored to the CAD navigation context.
        """
        was_numeric = False
        was_object_name = False
        was_new_object_name = False
        with cls._Lock:
            if Prompt is None or cls._ActivePrompt is Prompt:
                was_numeric = _RequiresNumericGrammar(cls._ActivePrompt)
                was_object_name = _RequiresObjectNameGrammar(cls._ActivePrompt)
                was_new_object_name = _RequiresNewObjectNameGrammar(cls._ActivePrompt)
                cls._ActivePrompt = None
        if was_numeric:
            NumericGrammarSwitcher.RestoreCadGrammar()
        elif was_object_name:
            ObjectNameGrammarSwitcher.RestoreCadGrammar()
        elif was_new_object_name:
            NewObjectNameGrammarSwitcher.RestoreCadGrammar()

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

    @staticmethod
    def _RunOnMainThread(Function) -> None:
        try:
            from integration.freecad_gui_bridge import run_on_main_thread

            run_on_main_thread(Function)
        except Exception:
            Function()

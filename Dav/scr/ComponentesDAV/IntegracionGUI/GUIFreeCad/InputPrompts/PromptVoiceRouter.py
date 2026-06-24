#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Route shared DAV voice recognition to the currently active input prompt."""

from __future__ import annotations

import threading
from typing import Any


class PromptVoiceRouter:
    """Thread-safe registry for the prompt currently collecting voice input."""

    _Lock = threading.RLock()
    _ActivePrompt: Any | None = None

    @classmethod
    def SetActivePrompt(cls, Prompt: Any) -> None:
        """Register a prompt as the active voice input target."""
        with cls._Lock:
            cls._ActivePrompt = Prompt

    @classmethod
    def ClearActivePrompt(cls, Prompt: Any | None = None) -> None:
        """Clear the active prompt, optionally only if it matches Prompt."""
        with cls._Lock:
            if Prompt is None or cls._ActivePrompt is Prompt:
                cls._ActivePrompt = None

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

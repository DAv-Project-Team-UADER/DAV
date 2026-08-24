#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Switches the active Vosk grammar in and out of numeric input mode."""

from __future__ import annotations


class NumericGrammarSwitcher:
    """Swaps the Vosk grammar between CAD navigation and numeric input.

    Kept separate from PromptVoiceRouter: the router's job is tracking which
    prompt is currently active, while grammar switching is a distinct
    responsibility with its own dependencies (DavVoiceService, the Numbers
    dictionary, the active Browser adapter).
    """

    @staticmethod
    def ActivateNumericGrammar() -> None:
        """Switch the Vosk grammar to numeric input words."""
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

    @staticmethod
    def RestoreCadGrammar() -> None:
        """Restore the Vosk grammar for the active Browser context."""
        try:
            from integration.browser_voice_adapter import get_active_adapter

            adapter = get_active_adapter()
            if adapter is not None:
                adapter.RestoreGrammar()
        except Exception:
            pass

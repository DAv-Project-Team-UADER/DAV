#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Switches the Vosk grammar to the vocabulary of dictatable object names."""

from __future__ import annotations


class NewObjectNameGrammarSwitcher:
    """Swaps the Vosk grammar to Dav/dic/ObjectNames while naming a new object.

    Naming a *new* object cannot reuse the document's labels: the name does
    not exist yet. Vosk only transcribes words in its active grammar, so the
    dictatable names come from a closed vocabulary that lives in the
    dictionary tree (ObjectNames/TraduceTo*.py), not in code.

    Sibling of ObjectNameGrammarSwitcher, which handles the opposite case:
    finding an object that already exists.
    """

    @staticmethod
    def ActivateNewObjectNameGrammar() -> None:
        """Load the object-name vocabulary into the recognizer."""
        try:
            from core.settings import settings
            from speech.dav_voice_service import DavVoiceService

            phrases = NewObjectNameGrammarSwitcher.CollectNamePhrases(
                getattr(settings, "language", "es")
            )
            if not phrases:
                return
            DavVoiceService.get().set_grammar(phrases)
        except Exception:
            # Nunca romper la creacion del objeto por un problema de gramatica.
            pass

    @staticmethod
    def CollectNamePhrases(language: str = "es") -> list[str]:
        """Return the dictatable names plus the words needed to confirm.

        Args:
            language: Two-letter language code.

        Returns:
            Spoken phrases for the recognizer, including '[unk]'.
        """
        phrases: set[str] = set()

        try:
            NewObjectNameGrammarSwitcher._EnsureDictionaryOnPath()
            from ObjectNames.ObjectNames import GetObjectNamePhrases

            phrases.update(GetObjectNamePhrases(language))
        except Exception:
            pass

        phrases.update(NewObjectNameGrammarSwitcher._NavigationPhrases(language))
        phrases.add("[unk]")
        return sorted(phrases)

    @staticmethod
    def _NavigationPhrases(language: str = "es") -> set[str]:
        """Confirm/cancel words for the active language only.

        SpokenNumberParser holds the three languages at once (so typing "ok"
        works with a Spanish UI), but the grammar must not: a word the model
        does not know cannot be recognised, yet it still competes and steals
        the ones that are valid. With the Spanish model, "accept" and "send"
        were crowding out "confirmar" and "entrar".
        """
        try:
            from InputPrompts.SpokenNumberParser import SpokenNumberParser
        except Exception:
            return set()

        words = set(SpokenNumberParser.ConfirmationWords)
        words.update(SpokenNumberParser.CancellationWords)
        try:
            from InputPrompts.GrammarLanguageFilter import BelongsToLanguage
        except Exception:
            return words
        return {w for w in words if BelongsToLanguage(w, language)}

    @staticmethod
    def _EnsureDictionaryOnPath() -> None:
        """Put Dav/dic on sys.path so the ObjectNames package resolves."""
        import sys

        from integration.voice_bootstrap import _resolve_dictionary_root

        root = str(_resolve_dictionary_root())
        if root not in sys.path:
            sys.path.insert(0, root)

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

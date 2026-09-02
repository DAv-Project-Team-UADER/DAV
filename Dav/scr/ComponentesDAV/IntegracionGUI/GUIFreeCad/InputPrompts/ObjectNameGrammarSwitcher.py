#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Switches the Vosk grammar to the labels of the active document's objects."""

from __future__ import annotations


class ObjectNameGrammarSwitcher:
    """Swaps the Vosk grammar between CAD navigation and object labels.

    Selecting an object by its dictated name only works when that name is in
    the recognizer's grammar: Vosk cannot transcribe a word it was not given.
    This adds the labels of the active document while a name prompt is open,
    then restores the navigation grammar.

    Follows NumericGrammarSwitcher: grammar switching is its own concern,
    separate from PromptVoiceRouter's job of tracking the active prompt.
    """

    @staticmethod
    def ActivateObjectNameGrammar() -> None:
        """Add the active document's object labels to the Vosk grammar.

        Labels are split into words: the grammar constrains vocabulary, not
        syntax, so a two-word label like "mesa chica" needs both words to be
        recognizable on their own.
        """
        try:
            from speech.dav_voice_service import DavVoiceService

            from core.settings import settings

            phrases = ObjectNameGrammarSwitcher.CollectLabelPhrases(
                getattr(settings, "language", "es")
            )
            if not phrases:
                return
            DavVoiceService.get().set_grammar(phrases)
        except Exception:
            # Nunca romper la creacion del objeto por un problema de gramatica.
            pass

    @staticmethod
    def CollectLabelPhrases(language: str = "es") -> list[str]:
        """Return the spoken phrases for every label in the active document.

        Returns:
            Lowercase labels plus their individual words, and the navigation
            words needed to confirm or cancel the prompt.
        """
        phrases: set[str] = set()

        try:
            import FreeCAD as App

            document = App.activeDocument()
        except Exception:
            document = None

        if document is not None:
            for obj in getattr(document, "Objects", []):
                label = str(getattr(obj, "Label", "") or "").strip().lower()
                if not label:
                    continue
                phrases.add(label)

                # Las palabras sueltas solo para etiquetas que puso el usuario.
                # Un rectangulo descompuesto deja 8 sub-elementos que meterian
                # "linea", "punto" y los numeros 1..4 en la gramatica, y esos
                # competidores le ganan el audio al nombre que el usuario
                # realmente quiere decir (ver pendientes-dav.md §14).
                if ObjectNameGrammarSwitcher._IsGeneratedLabel(label):
                    continue
                for word in label.split():
                    if word:
                        phrases.add(word)

        phrases.update(ObjectNameGrammarSwitcher._NavigationPhrases(language))
        phrases.add("[unk]")
        return sorted(phrases)

    @staticmethod
    def _IsGeneratedLabel(label: str) -> bool:
        """Return True for a label the Tagger produced, not the user.

        Tagger labels are '<kind> <number>' ("Linea 1", "Punto 3"), one per
        sub-element of a decomposed shape. They stay reachable by their full
        label; only their individual words are kept out of the grammar.
        """
        parts = label.strip().lower().split()
        if len(parts) != 2 or not parts[1].isdigit():
            return False

        try:
            from InputPrompts.NewObjectNameGrammarSwitcher import (
                NewObjectNameGrammarSwitcher,
            )

            NewObjectNameGrammarSwitcher._EnsureDictionaryOnPath()
            from Tagger.TaggerKinds import GeneratedLabelWords

            return parts[0] in GeneratedLabelWords()
        except Exception:
            # Sin el diccionario, no se descarta nada: es preferible una
            # gramatica con ruido a una que pierda un nombre del usuario.
            return False

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
    def RestoreCadGrammar() -> None:
        """Restore the Vosk grammar for the active Browser context."""
        try:
            from integration.browser_voice_adapter import get_active_adapter

            adapter = get_active_adapter()
            if adapter is not None:
                adapter.RestoreGrammar()
        except Exception:
            pass

#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Object selection prompt for DAV voice-driven parameter collection."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Callable

from InputPrompts.BaseInputPrompt import BaseInputPrompt
from InputPrompts.PromptResult import PromptResult
from InputPrompts.SpokenNumberParser import SpokenNumberParser
from InputPrompts.InputPromptI18n import KindLabel, ResolveLanguage, T


class ObjectSelectionInputPrompt(BaseInputPrompt):
    """Prompt that guides the user through FreeCAD object selection."""

    NextWords: set[str] = {
        "siguiente",
        "otro",
        "otra",
        "avanzar",
        "proximo",
        "proxima",
        "next",
        "other",
        "advance",
        "seguinte",
        "outro",
        "outra",
        "proximo",
        "proxima",
    }

    SelectWords: set[str] = {
        "seleccionar",
        "selecciona",
        "select",
        "choose",
        "elegir",
        "elige",
        "escolher",
        "escolha",
    }

    # «buscar por deletreo»: Vosk a veces pierde «por» o confunde «deletreo», por eso
    # alcanza con cualquiera de estas palabras sueltas.
    SearchWords: set[str] = {
        "deletreo",
        "deletrear",
        "deletrea",
        "buscar",
        "busca",
        "search",
        "spell",
        "spelling",
        "find",
        "soletrar",
        "soletracao",
        "procurar",
    }

    _GrammarWords: dict[str, list[str]] = {
        "es": ["avanzar", "siguiente", "otro", "otra", "seleccionar", "elegir",
               "buscar", "buscar por deletreo", "por deletreo", "deletreo", "deletrear"],
        "en": ["advance", "next", "other", "select", "choose",
               "search", "search by spelling", "spell", "spelling", "find"],
        "pt": ["avancar", "avançar", "seguinte", "outro", "outra", "escolher",
               "procurar", "soletrar"],
    }

    # Cuántas alternativas se nombran en pantalla además de la elegida.
    SearchAlternatives: int = 2

    def __init__(
        self,
        Title: str | None = None,
        Message: str | None = None,
        Parent=None,
        ReturnObject: bool = False,
        ObjectFilter: Callable[[Any], bool] | None = None,
    ) -> None:
        language = ResolveLanguage()
        super().__init__(
            Title or T(language, "param_title", index="obj"),
            Message or T(language, "param_message", kind=KindLabel(language, "object"), name="object"),
            Parent,
        )
        self._ReturnObject = ReturnObject
        # Si se pasa, solo se ofrecen los objetos para los que devuelve True.
        self._ObjectFilter = ObjectFilter
        self._Selector: Any | None = None
        self._ObjectNames: list[str] = []
        self._CurrentIndex = -1
        self._InitializeSelection()

    def _InitializeSelection(self) -> None:
        try:
            App = self._ImportFreeCADApp()
            ObjectSelection = self._ImportObjectSelection()
        except Exception as error:
            self.Fail(T(self._Language, "object_unavailable", error=error))
            return

        document = App.activeDocument()
        if document is None:
            self.Fail(T(self._Language, "object_no_doc"))
            return

        self._ObjectNames = [
            obj.Name
            for obj in getattr(document, "Objects", [])
            if self._ObjectFilter is None or self._ObjectFilter(obj)
        ]
        if not self._ObjectNames:
            self.Fail(T(self._Language, "object_no_objects"))
            return

        self._Selector = ObjectSelection()
        self._Selector.VectorSelection(self._ObjectNames)
        self.SetStatus(T(self._Language, "object_browse_confirm"))
        self._SelectNextObject()

    @classmethod
    def GrammarPhrases(cls, Language: str) -> list[str]:
        """Return the Vosk phrases: browse, search by spelling, select, confirm, cancel.

        Sin esto la lista corre con la gramática del contexto CAD, que no trae
        «avanzar» ni «buscar por deletreo», y el reconocedor nunca las oye.
        """
        from InputPrompts.PlaneGrammarSwitcher import PlaneGrammarSwitcher

        phrases = list(cls._GrammarWords.get(Language, cls._GrammarWords["es"]))
        phrases.extend(PlaneGrammarSwitcher.PlanePhrases(Language)[2:])
        seen: set[str] = set()
        return [word for word in phrases if not (word in seen or seen.add(word))]

    def ProcessFinalText(self, Text: str) -> PromptResult:
        """Handle voice commands for browsing and confirming object selection."""
        self.SetHeardText(Text)
        tokens = SpokenNumberParser.Tokenize(Text)

        if self._HasCancellation(tokens):
            return self.Cancel()

        if any(token in self.SearchWords for token in tokens):
            self._SearchBySpelling()
            self._Result = PromptResult.Pending()
            return self.GetResult()

        if any(token in self.NextWords for token in tokens):
            self._SelectNextObject()
            self._Result = PromptResult.Pending()
            return self.GetResult()

        if self._HasConfirmation(tokens) or any(token in self.SelectWords for token in tokens):
            return self._AcceptCurrentObject()

        self.SetStatus(T(self._Language, "object_browse"))
        return self.GetResult()

    def GetSelectedObjectName(self) -> str | None:
        """Return the currently highlighted object name."""
        if self._CurrentIndex < 0 or not self._ObjectNames:
            return None
        return self._ObjectNames[self._CurrentIndex]

    def _SelectNextObject(self) -> None:
        if not self._ObjectNames or self._Selector is None:
            return
        if self._SelectIndex((self._CurrentIndex + 1) % len(self._ObjectNames)):
            self._ShowSelected()

    def _SelectIndex(self, Index: int) -> bool:
        """Highlight the object at ``Index`` in the 3D view; False when it failed."""
        try:
            self._Selector._CurrentIndex = Index
            self._Selector.SelectOther = True
            self._CurrentIndex = (self._Selector._CurrentIndex - 1) % len(self._ObjectNames)
        except Exception as error:
            self.Fail(T(self._Language, "object_select_error", error=error))
            return False
        return True

    def _ShowSelected(self) -> None:
        current_name = self._ObjectNames[self._CurrentIndex]
        self.SetHeardText(current_name)
        self.SetStatus(
            T(
                self._Language,
                "object_selected",
                name=current_name,
                current=self._CurrentIndex + 1,
                total=len(self._ObjectNames),
            )
        )

    def _SearchBySpelling(self) -> None:
        """Ask for a spelled name and jump to the object that looks most like it."""
        if not self._ObjectNames or self._Selector is None:
            return
        spelled = self._AskSpelling()
        if not spelled:
            self.SetStatus(T(self._Language, "object_browse"))
            return

        SpellMatch = self._ImportSpellMatch()
        document = self._ImportFreeCADApp().activeDocument()
        labels = []
        for name in self._ObjectNames:
            obj = document.getObject(name) if document is not None else None
            labels.append((name, getattr(obj, "Label", name)))
        ranked = SpellMatch.RankMatches(spelled, labels, Limit=1 + self.SearchAlternatives)
        if not ranked:
            self.SetHeardText(spelled)
            self.SetStatus(T(self._Language, "object_search_none", text=spelled))
            return
        if not self._SelectIndex(ranked[0][0]):
            return

        best_name = self._ObjectNames[self._CurrentIndex]
        others = [self._ObjectNames[index] for index, _score in ranked[1:]]
        self.SetHeardText(best_name)
        self.SetStatus(
            T(
                self._Language,
                "object_search_found",
                text=spelled,
                name=best_name,
                current=self._CurrentIndex + 1,
                total=len(self._ObjectNames),
                others=T(self._Language, "object_search_others", names=", ".join(others)) if others else "",
            )
        )

    def _AskSpelling(self) -> str | None:
        """Open the letter-by-letter dialog on top of this one; None when cancelled.

        Al cerrarse, la voz vuelve a este diálogo y la gramática al contexto CAD.
        """
        from InputPrompts.PlaneGrammarSwitcher import PlaneGrammarSwitcher
        from InputPrompts.PromptVoiceRouter import PromptVoiceRouter
        from InputPrompts.SpellingInputPrompt import SpellingInputPrompt

        prompt = SpellingInputPrompt(
            Title=T(self._Language, "object_search_title"),
            Message=T(self._Language, "object_search_message"),
            Parent=self,
        )
        previous = PromptVoiceRouter.GetActivePrompt()
        PlaneGrammarSwitcher.ActivateGrammar(SpellingInputPrompt.GrammarPhrases(PlaneGrammarSwitcher.CurrentLanguage()))
        PromptVoiceRouter.SetActivePrompt(prompt)
        try:
            result = prompt.RequestValue()
        finally:
            if previous is None:
                PromptVoiceRouter.ClearActivePrompt(prompt)
            else:
                PromptVoiceRouter.SetActivePrompt(previous)
            # la voz vuelve a la lista: su gramática, no la del contexto CAD
            PlaneGrammarSwitcher.ActivateGrammar(self.GrammarPhrases(PlaneGrammarSwitcher.CurrentLanguage()))
        if result is None or result.Cancelled or not result.Success:
            return None
        return str(result.Value)

    def _AcceptCurrentObject(self) -> PromptResult:
        if self._CurrentIndex < 0 or not self._ObjectNames:
            return self.Fail(T(self._Language, "object_none"))

        current_name = self._ObjectNames[self._CurrentIndex]
        value = self._ResolveObject(current_name) if self._ReturnObject else current_name
        if value is None:
            value = current_name
        return self.AcceptValue(value)

    def _ResolveObject(self, ObjectName: str) -> Any | None:
        try:
            App = self._ImportFreeCADApp()
            document = App.activeDocument()
            if document is None:
                return None
            return document.getObject(ObjectName)
        except Exception:
            return None

    @staticmethod
    def _ImportFreeCADApp():
        import FreeCAD as App

        return App

    @staticmethod
    def _ImportSpellMatch():
        try:
            from selection import spell_match

            return spell_match
        except ImportError:
            # mismo camino que ObjectSelection: la carpeta que contiene a selection/
            ObjectSelectionInputPrompt._ImportObjectSelection()
            from selection import spell_match

            return spell_match

    @staticmethod
    def _ImportObjectSelection():
        try:
            from selection.object_selection import ObjectSelection

            return ObjectSelection
        except ImportError:
            selection_root = Path(__file__).resolve()
            for parent in selection_root.parents:
                candidate = parent / "selection"
                if (candidate / "object_selection.py").is_file():
                    selection_root = candidate.parent
                    break
            else:
                selection_root = Path(__file__).resolve().parents[3]

            if selection_root.is_dir():
                selection_text = str(selection_root)
                if selection_text not in sys.path:
                    sys.path.insert(0, selection_text)
            from selection.object_selection import ObjectSelection

            return ObjectSelection

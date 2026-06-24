#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Object selection prompt for DAV voice-driven parameter collection."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from InputPrompts.BaseInputPrompt import BaseInputPrompt
from InputPrompts.PromptResult import PromptResult
from InputPrompts.SpokenNumberParser import SpokenNumberParser


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

    def __init__(
        self,
        Title: str = "DAV Object Selection",
        Message: str = "Select an object",
        Parent=None,
        ReturnObject: bool = False,
    ) -> None:
        super().__init__(Title, Message, Parent)
        self._ReturnObject = ReturnObject
        self._Selector: Any | None = None
        self._ObjectNames: list[str] = []
        self._CurrentIndex = -1
        self._InitializeSelection()

    def _InitializeSelection(self) -> None:
        try:
            App = self._ImportFreeCADApp()
            ObjectSelection = self._ImportObjectSelection()
        except Exception as error:
            self.Fail(f"Object selection is not available: {error}")
            return

        document = App.activeDocument()
        if document is None:
            self.Fail("No active FreeCAD document.")
            return

        self._ObjectNames = [obj.Name for obj in getattr(document, "Objects", [])]
        if not self._ObjectNames:
            self.Fail("The active FreeCAD document has no objects.")
            return

        self._Selector = ObjectSelection()
        self._Selector.VectorSelection(self._ObjectNames)
        self.SetStatus("Say next to browse objects, then enter or send to confirm.")
        self._SelectNextObject()

    def ProcessFinalText(self, Text: str) -> PromptResult:
        """Handle voice commands for browsing and confirming object selection."""
        self.SetHeardText(Text)
        tokens = SpokenNumberParser.Tokenize(Text)

        if self._HasCancellation(tokens):
            return self.Cancel()

        if any(token in self.NextWords for token in tokens):
            self._SelectNextObject()
            self._Result = PromptResult.Pending()
            return self.GetResult()

        if self._HasConfirmation(tokens) or any(token in self.SelectWords for token in tokens):
            return self._AcceptCurrentObject()

        self.SetStatus("Say next to browse, or enter/send to confirm.")
        return self.GetResult()

    def GetSelectedObjectName(self) -> str | None:
        """Return the currently highlighted object name."""
        if self._CurrentIndex < 0 or not self._ObjectNames:
            return None
        return self._ObjectNames[self._CurrentIndex]

    def _SelectNextObject(self) -> None:
        if not self._ObjectNames or self._Selector is None:
            return

        self._CurrentIndex = (self._CurrentIndex + 1) % len(self._ObjectNames)
        current_name = self._ObjectNames[self._CurrentIndex]

        try:
            self._Selector._CurrentIndex = self._CurrentIndex
            self._Selector.SelectOther = True
            self._CurrentIndex = (self._Selector._CurrentIndex - 1) % len(self._ObjectNames)
            current_name = self._ObjectNames[self._CurrentIndex]
        except Exception as error:
            self.Fail(f"Could not select object: {error}")
            return

        self.SetHeardText(current_name)
        self.SetStatus(
            f"Selected {current_name} ({self._CurrentIndex + 1}/{len(self._ObjectNames)})."
        )

    def _AcceptCurrentObject(self) -> PromptResult:
        if self._CurrentIndex < 0 or not self._ObjectNames:
            return self.Fail("No object is currently selected.")

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
    def _HasConfirmation(Tokens: list[str]) -> bool:
        return any(token in SpokenNumberParser.ConfirmationWords for token in Tokens)

    @staticmethod
    def _HasCancellation(Tokens: list[str]) -> bool:
        return any(token in SpokenNumberParser.CancellationWords for token in Tokens)

    @staticmethod
    def _ImportFreeCADApp():
        import FreeCAD as App

        return App

    @staticmethod
    def _ImportObjectSelection():
        try:
            from selection import ObjectSelection

            return ObjectSelection
        except ImportError:
            selection_root = Path(__file__).resolve()
            for parent in selection_root.parents:
                candidate = parent / "selection"
                if (candidate / "selection.py").is_file():
                    selection_root = candidate
                    break
            else:
                selection_root = Path(__file__).resolve().parents[3] / "selection"

            if selection_root.is_dir():
                selection_text = str(selection_root)
                if selection_text not in sys.path:
                    sys.path.insert(0, selection_text)
            from selection import ObjectSelection

            return ObjectSelection

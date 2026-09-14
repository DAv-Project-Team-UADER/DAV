#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Voice-driven sketch plane orientation selector for DAV."""

from __future__ import annotations

from typing import Any

from InputPrompts.BaseInputPrompt import BaseInputPrompt
from InputPrompts.PromptResult import PromptResult
from InputPrompts.SpokenNumberParser import SpokenNumberParser


class PlaneSelectionInputPrompt(BaseInputPrompt):
    """Prompt to choose the sketch plane orientation (XY / XZ / YZ) by voice.

    Replaces FreeCAD's native ``SketchOrientationDialog`` when creating a new
    sketch, because that dialog is not reachable from the DAV voice pipeline.
    The user browses the three axes with ``arriba``/``abajo`` (up/down),
    highlights the current selection, and confirms with any confirmation word
    (``okey``/``ok``/``enviar``/``aceptar``/``listo``/``vale``/etc.) or
    cancels with ``cancelar``/``descartar``/``no``/etc. The sets are shared
    with ``SpokenNumberParser`` and ``NavCommands`` so adding a synonym there
    automatically works here.

    The accepted value is one of the plane keys ``XY``, ``XZ`` or ``YZ``.
    """

    PlaneKeys: tuple[str, ...] = ("XY", "XZ", "YZ")

    UpWords: set[str] = {
        "arriba",
        "subir",
        "anterior",
        "previo",
        "previa",
        "before",
        "previous",
        "up",
        "cima",
        "acima",
        "voltar",
        "back",
    }

    DownWords: set[str] = {
        "abajo",
        "bajar",
        "siguiente",
        "proximo",
        "proxima",
        "next",
        "advance",
        "down",
        "abaixo",
        "seguinte",
    }

    # Sinónimos extra de confirmación propios del selector; ahora
    # SpokenNumberParser ya incluye "okey"/"okay", pero se mantienen acá
    # por compatibilidad y para que el selector siga aceptando "okey"
    # aunque el módulo de números no se haya cargado todavía.
    OkeyWords: set[str] = {"okey", "okay", "ok"}

    def __init__(
        self,
        Title: str = "DAV Sketch Orientation",
        Message: str = "Elegí el plano del boceto (XY, XZ o YZ)",
        Parent=None,
    ) -> None:
        super().__init__(Title, Message, Parent)
        self._CurrentIndex = 0
        self._Plane = self.PlaneKeys[self._CurrentIndex]
        self.SetStatus(self._StatusText())
        self.SetHeardText(self._Plane)

    def ProcessPartialText(self, Text: str) -> None:
        """Preview recognized text without acting on it."""
        self.SetHeardText(Text)
        self.SetStatus(self._StatusText())

    def ProcessFinalText(self, Text: str) -> PromptResult:
        """Handle up/down navigation and okey/cancel confirmation."""
        self.SetHeardText(Text)
        tokens = SpokenNumberParser.Tokenize(Text)
        tokens_set = set(tokens)

        if tokens_set & self.CancellationWords:
            return self.Cancel()

        if tokens_set & self.DownWords:
            self._Step(1)
            self._Result = PromptResult.Pending()
            self.SetStatus(self._StatusText())
            return self.GetResult()

        if tokens_set & self.UpWords:
            self._Step(-1)
            self._Result = PromptResult.Pending()
            self.SetStatus(self._StatusText())
            return self.GetResult()

        if tokens_set & self.OkeyWords or self._HasConfirmation(tokens):
            return self.AcceptValue(self._Plane)

        self.SetStatus("Decí arriba o abajo, y después okey/enviar/listos para confirmar, cancelar para salir.")
        return self.GetResult()

    @property
    def CancellationWords(self) -> set[str]:
        """Return the shared cancellation words."""
        return SpokenNumberParser.CancellationWords

    def GetSelectedPlane(self) -> str:
        """Return the currently highlighted plane key (XY, XZ or YZ)."""
        return self._Plane

    def _Step(self, Direction: int) -> None:
        total = len(self.PlaneKeys)
        self._CurrentIndex = (self._CurrentIndex + Direction) % total
        self._Plane = self.PlaneKeys[self._CurrentIndex]
        self.SetHeardText(self._Plane)

    def _StatusText(self) -> str:
        return (
            f"Plano {self._Plane} ({self._CurrentIndex + 1}/{len(self.PlaneKeys)})"
            " — decí arriba o abajo, okey/enviar para confirmar, cancelar para salir."
        )

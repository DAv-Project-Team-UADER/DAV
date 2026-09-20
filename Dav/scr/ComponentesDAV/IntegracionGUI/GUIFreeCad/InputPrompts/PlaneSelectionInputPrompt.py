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
    When ``ExtraOptions`` is given (for example the planar faces of the solid
    being edited) those entries come after the three planes and the accepted
    value can also be one of their keys.
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
        ExtraOptions: list[tuple[str, str]] | None = None,
    ) -> None:
        """Build the prompt.

        Args:
            Title: Window title.
            Message: Instruction shown to the user.
            Parent: Optional Qt parent widget.
            ExtraOptions: Additional ``(key, label)`` choices listed after the
                three planes, e.g. ``[("Face3", "Cara superior")]``. The key is
                what the prompt returns; the label is what the user sees.
        """
        super().__init__(Title, Message, Parent)
        # Los planos van primero, tal como estaban; las opciones extra
        # (caras) se suman después sin cambiar el orden de los planos.
        self._Options: list[tuple[str, str]] = [(key, key) for key in self.PlaneKeys]
        self._Options.extend(ExtraOptions or [])
        self._CurrentIndex = 0
        self._Plane = self._Options[self._CurrentIndex][0]
        self.SetStatus(self._StatusText())
        self.SetHeardText(self._Label())

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
        """Return the key of the highlighted option (XY, XZ, YZ or an extra key)."""
        return self._Plane

    def _Label(self) -> str:
        """Return the text shown for the highlighted option."""
        return self._Options[self._CurrentIndex][1]

    def _Step(self, Direction: int) -> None:
        total = len(self._Options)
        self._CurrentIndex = (self._CurrentIndex + Direction) % total
        self._Plane = self._Options[self._CurrentIndex][0]
        self.SetHeardText(self._Label())

    def _StatusText(self) -> str:
        # los planos conservan el texto de siempre ("Plano XY"); las caras
        # ya traen su propia etiqueta ("Cara superior")
        name = f"Plano {self._Plane}" if self._Plane in self.PlaneKeys else self._Label()
        return (
            f"{name} ({self._CurrentIndex + 1}/{len(self._Options)})"
            " — decí arriba o abajo, okey/enviar para confirmar, cancelar para salir."
        )

#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""String input prompt for DAV voice-driven parameter collection."""

from __future__ import annotations

from InputPrompts.BaseInputPrompt import BaseInputPrompt
from InputPrompts.PromptResult import PromptResult
from InputPrompts.SpokenNumberParser import SpokenNumberParser


class StringInputPrompt(BaseInputPrompt):
    """Prompt that captures a free text value."""

    def __init__(
        self,
        Title: str = "DAV Text Input",
        Message: str = "Say a text value",
        Parent=None,
    ) -> None:
        super().__init__(Title, Message, Parent)

    def ProcessFinalText(self, Text: str) -> PromptResult:
        """Accumulate spoken text and accept it once a confirmation arrives.

        Accumulates across utterances, like NumericInputPrompt: saying the
        name and then "aceptar" as two separate phrases has to work. Without
        this the confirmation arrived on its own, with the name already gone,
        and the value came out empty.
        """
        tokens = SpokenNumberParser.Tokenize(Text)

        if self._HasCancellation(tokens):
            self._AccumulatedText = ""
            return self.Cancel()

        if self._HasConfirmation(tokens):
            # La confirmacion puede venir sola ("aceptar") o cerrando la misma
            # frase ("rectangulo aceptar"): se toma lo acumulado mas lo que
            # traiga esta frase antes de la palabra de confirmacion.
            spoken_now = self._StripConfirmation(Text)
            value = " ".join(part for part in (self._AccumulatedText, spoken_now) if part)
            value = value.strip()
            self._AccumulatedText = ""
            if not value:
                self.SetStatus("No hay texto para confirmar. Diga un nombre primero.")
                return self.GetResult()
            self.SetHeardText(value)
            return self.AcceptValue(value)

        self._AccumulatedText = (
            (self._AccumulatedText + " " + Text).strip() if self._AccumulatedText else Text
        )
        self.SetHeardText(self._AccumulatedText)
        self.SetStatus("Diga aceptar o enviar para confirmar.")
        return self.GetResult()

    @staticmethod
    def _StripConfirmation(Text: str) -> str:
        words = Text.strip().split()
        while words:
            normalized = SpokenNumberParser.NormalizeText(words[-1])
            if normalized not in SpokenNumberParser.ConfirmationWords:
                break
            words.pop()
        return " ".join(words).strip()

#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Integer input prompt for DAV voice-driven parameter collection."""

from __future__ import annotations

from InputPrompts.BaseInputPrompt import BaseInputPrompt
from InputPrompts.PromptResult import PromptResult
from InputPrompts.SpokenNumberParser import SpokenNumberParser


class IntegerInputPrompt(BaseInputPrompt):
    """Prompt that captures and validates an integer value."""

    def __init__(
        self,
        Title: str = "DAV Integer Input",
        Message: str = "Say an integer value",
        Parent=None,
    ) -> None:
        super().__init__(Title, Message, Parent)

    def ProcessFinalText(self, Text: str) -> PromptResult:
        """Parse final recognized text and accept it as an integer when valid."""
        self.SetHeardText(Text)
        tokens = SpokenNumberParser.Tokenize(Text)

        if self._HasCancellation(tokens):
            return self.Cancel()

        if not self._HasConfirmation(tokens):
            self.SetStatus("Waiting for enter or send...")
            return self.GetResult()

        try:
            value = SpokenNumberParser.ParseInteger(Text)
        except ValueError as error:
            return self.Fail(str(error))

        return self.AcceptValue(value)

    @staticmethod
    def _HasConfirmation(Tokens: list[str]) -> bool:
        return any(token in SpokenNumberParser.ConfirmationWords for token in Tokens)

    @staticmethod
    def _HasCancellation(Tokens: list[str]) -> bool:
        return any(token in SpokenNumberParser.CancellationWords for token in Tokens)

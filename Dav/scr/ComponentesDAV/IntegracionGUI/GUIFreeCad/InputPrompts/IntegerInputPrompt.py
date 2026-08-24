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
        """Parse final recognized text and accept it as an integer when valid.

        Accumulates text across multiple utterances so that saying a number
        and then "ok" in separate phrases works correctly (e.g. "cinco"
        followed by "ok" produces 5).
        """
        tokens = SpokenNumberParser.Tokenize(Text)

        if self._HasCancellation(tokens):
            self._AccumulatedText = ""
            return self.Cancel()

        if self._HasConfirmation(tokens):
            if not self._AccumulatedText:
                self.SetStatus("No value to confirm. Say a number first.")
                return self.GetResult()
            parse_text = self._AccumulatedText
            self._AccumulatedText = ""
            try:
                value = SpokenNumberParser.ParseInteger(parse_text)
            except ValueError as error:
                return self.Fail(str(error))
            return self.AcceptValue(value)

        self._AccumulatedText = (
            (self._AccumulatedText + " " + Text).strip() if self._AccumulatedText else Text
        )
        self.SetStatus("Say a number, then say ok or send.")
        return self.GetResult()

    @staticmethod
    def _HasConfirmation(Tokens: list[str]) -> bool:
        return any(token in SpokenNumberParser.ConfirmationWords for token in Tokens)

    @staticmethod
    def _HasCancellation(Tokens: list[str]) -> bool:
        return any(token in SpokenNumberParser.CancellationWords for token in Tokens)

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

    def VoiceGrammarPhrases(self) -> list[str]:
        return SpokenNumberParser.GrammarPhrases()

    def ProcessFinalText(self, Text: str) -> PromptResult:
        """Parse final recognized text and accept it as an integer when valid."""
        tokens = SpokenNumberParser.Tokenize(Text)

        if self._HasCancellation(tokens):
            return self.Cancel()

        combined = self._CombineWithPrevious(Text, tokens)
        self.SetHeardText(combined)

        if not self._HasConfirmation(SpokenNumberParser.Tokenize(combined)):
            self.SetStatus("Waiting for enter or send...")
            return self.GetResult()

        try:
            value = SpokenNumberParser.ParseInteger(combined)
        except ValueError as error:
            return self.Fail(str(error))

        return self.AcceptValue(value)

    def _CombineWithPrevious(self, Text: str, Tokens: list[str]) -> str:
        previous = self.GetCurrentText()
        if not previous or previous == Text:
            return Text
        number_tokens = [
            token
            for token in Tokens
            if token not in SpokenNumberParser.ConfirmationWords
            and token not in SpokenNumberParser.CancellationWords
        ]
        if self._HasConfirmation(Tokens) and not number_tokens:
            return f"{previous} {Text}".strip()
        return Text

    @staticmethod
    def _HasConfirmation(Tokens: list[str]) -> bool:
        return any(token in SpokenNumberParser.ConfirmationWords for token in Tokens)

    @staticmethod
    def _HasCancellation(Tokens: list[str]) -> bool:
        return any(token in SpokenNumberParser.CancellationWords for token in Tokens)

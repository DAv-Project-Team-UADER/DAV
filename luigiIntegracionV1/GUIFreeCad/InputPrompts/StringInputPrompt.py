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
        """Accept final recognized text after a confirmation word."""
        super().ProcessFinalText(Text)
        full_text = self._AccumulatedText
        tokens = SpokenNumberParser.Tokenize(full_text)

        if self._HasCancellation(tokens):
            return self.Cancel()

        if not self._HasConfirmation(tokens):
            self.SetStatus("Waiting for enter or send...")
            return self.GetResult()

        value = self._StripConfirmation(full_text)
        if not value:
            self._AccumulatedText = ""
            self.SetHeardText("")
            return self.Fail("Text value cannot be empty.")

        return self.AcceptValue(value)

    @staticmethod
    def _HasConfirmation(Tokens: list[str]) -> bool:
        return any(token in SpokenNumberParser.ConfirmationWords for token in Tokens)

    @staticmethod
    def _HasCancellation(Tokens: list[str]) -> bool:
        return any(token in SpokenNumberParser.CancellationWords for token in Tokens)

    @staticmethod
    def _StripConfirmation(Text: str) -> str:
        words = Text.strip().split()
        while words:
            normalized = SpokenNumberParser.NormalizeText(words[-1])
            if normalized not in SpokenNumberParser.ConfirmationWords:
                break
            words.pop()
        return " ".join(words).strip()

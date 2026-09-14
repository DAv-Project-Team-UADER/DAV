#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""String input prompt for DAV voice-driven parameter collection."""

from __future__ import annotations

from InputPrompts.BaseInputPrompt import BaseInputPrompt
from InputPrompts.PromptResult import PromptResult
from InputPrompts.SpokenNumberParser import SpokenNumberParser
from InputPrompts.InputPromptI18n import KindLabel, ResolveLanguage, T


class StringInputPrompt(BaseInputPrompt):
    """Prompt that captures a free text value."""

    def __init__(
        self,
        Title: str | None = None,
        Message: str | None = None,
        Parent=None,
    ) -> None:
        language = ResolveLanguage()
        super().__init__(
            Title or T(language, "param_title", index="str"),
            Message or T(language, "param_message", kind=KindLabel(language, "str"), name="label"),
            Parent,
        )

    def ProcessFinalText(self, Text: str) -> PromptResult:
        """Accept final recognized text after a confirmation word."""
        self.SetHeardText(Text)
        tokens = SpokenNumberParser.Tokenize(Text)

        if self._HasCancellation(tokens):
            return self.Cancel()

        if not self._HasConfirmation(tokens):
            self.SetStatus(T(self._Language, "string_waiting"))
            return self.GetResult()

        value = self._StripConfirmation(Text)
        if not value:
            return self.Fail(T(self._Language, "string_not_empty"))

        return self.AcceptValue(value)

    @staticmethod
    def _StripConfirmation(Text: str) -> str:
        words = Text.strip().split()
        while words:
            normalized = SpokenNumberParser.NormalizeText(words[-1])
            if normalized not in SpokenNumberParser.ConfirmationWords:
                break
            words.pop()
        return " ".join(words).strip()

#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Integer input prompt for DAV voice-driven parameter collection."""

from __future__ import annotations

from InputPrompts.NumericInputPrompt import NumericInputPrompt
from InputPrompts.SpokenNumberParser import SpokenNumberParser
from InputPrompts.InputPromptI18n import KindLabel, ResolveLanguage, T


class IntegerInputPrompt(NumericInputPrompt):
    """Prompt that captures and validates an integer value."""

    def __init__(
        self,
        Title: str | None = None,
        Message: str | None = None,
        Parent=None,
    ) -> None:
        language = ResolveLanguage()
        super().__init__(
            Title or T(language, "param_title", index="int"),
            Message or T(language, "param_message", kind=KindLabel(language, "int"), name="sides"),
            Parent,
        )

    def _ParseAccumulatedText(self, Text: str) -> int:
        return SpokenNumberParser.ParseInteger(Text)

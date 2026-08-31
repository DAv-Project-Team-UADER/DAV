#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Integer input prompt for DAV voice-driven parameter collection."""

from __future__ import annotations

from InputPrompts.NumericInputPrompt import NumericInputPrompt
from InputPrompts.SpokenNumberParser import SpokenNumberParser


class IntegerInputPrompt(NumericInputPrompt):
    """Prompt that captures and validates an integer value."""

    def __init__(
        self,
        Title: str = "DAV Integer Input",
        Message: str = "Say an integer value",
        Parent=None,
    ) -> None:
        super().__init__(Title, Message, Parent)

    def _ParseAccumulatedText(self, Text: str) -> int:
        return SpokenNumberParser.ParseInteger(Text)

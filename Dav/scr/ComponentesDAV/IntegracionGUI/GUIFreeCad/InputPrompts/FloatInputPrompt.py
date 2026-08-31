#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Float input prompt for DAV voice-driven parameter collection."""

from __future__ import annotations

from InputPrompts.NumericInputPrompt import NumericInputPrompt
from InputPrompts.SpokenNumberParser import SpokenNumberParser


class FloatInputPrompt(NumericInputPrompt):
    """Prompt that captures and validates a floating-point value."""

    def __init__(
        self,
        Title: str = "DAV Float Input",
        Message: str = "Say a decimal value",
        Parent=None,
    ) -> None:
        super().__init__(Title, Message, Parent)

    def _ParseAccumulatedText(self, Text: str) -> float:
        return SpokenNumberParser.ParseFloat(Text)

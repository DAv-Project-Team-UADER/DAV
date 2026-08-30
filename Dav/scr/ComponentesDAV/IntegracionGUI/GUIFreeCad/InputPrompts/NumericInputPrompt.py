#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Shared base for prompts that accumulate spoken digits before parsing."""

from __future__ import annotations

from InputPrompts.BaseInputPrompt import BaseInputPrompt
from InputPrompts.PromptResult import PromptResult
from InputPrompts.SpokenNumberParser import SpokenNumberParser


class NumericInputPrompt(BaseInputPrompt):
    """Template for prompts that collect a number across several utterances.

    Concrete prompts (Integer, Float) only implement `_ParseAccumulatedText`;
    the accumulate/confirm/cancel voice flow lives here so a new numeric
    prompt type does not need to copy it.
    """

    def RequiresNumericGrammar(self) -> bool:
        return True

    def ProcessFinalText(self, Text: str) -> PromptResult:
        """Accumulate spoken text and parse it once a confirmation word arrives.

        Accumulates text across multiple utterances so that saying a number
        and then "ok" in separate phrases works correctly (e.g. "cinco"
        followed by "ok" produces the parsed value).
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
                value = self._ParseAccumulatedText(parse_text)
            except ValueError as error:
                return self.Fail(str(error))
            return self.AcceptValue(value)

        self._AccumulatedText = (
            (self._AccumulatedText + " " + Text).strip() if self._AccumulatedText else Text
        )
        self.SetStatus("Say a number, then say ok or send.")
        return self.GetResult()

    def _ParseAccumulatedText(self, Text: str):
        """Parse the accumulated spoken text into a numeric value.

        Subclasses must override this to return their concrete numeric type.
        """
        raise NotImplementedError

#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Prompt used to dictate the name of a newly created object."""

from __future__ import annotations

from InputPrompts.PromptResult import PromptResult
from InputPrompts.StringInputPrompt import StringInputPrompt


class NewObjectNameInputPrompt(StringInputPrompt):
    """String prompt restricted to the ObjectNames vocabulary.

    A new object has no name yet, so there is nothing in the document to
    listen for. The recognizer is given a closed vocabulary instead (see
    Dav/dic/ObjectNames), and what the user says is mapped to its written
    form through it.
    """

    def __init__(
        self,
        Title: str = "DAV Object Name",
        Message: str = "Say a name for the object",
        Parent=None,
        Language: str = "es",
    ) -> None:
        super().__init__(Title, Message, Parent)
        self._Language = Language

    def RequiresNewObjectNameGrammar(self) -> bool:
        """Return True so the router swaps in the object-name vocabulary."""
        return True

    def ProcessFinalText(self, Text: str) -> PromptResult:
        """Accept the dictated name, mapped to its canonical written form."""
        result = super().ProcessFinalText(Text)
        if not result.Success:
            return result

        canonical = self._ResolveName(str(result.Value or ""))
        if not canonical:
            # Se reconocio algo que no esta en el vocabulario: se toma tal cual
            # en vez de descartarlo, asi un nombre util no se pierde.
            return result
        return self.AcceptValue(canonical)

    def _ResolveName(self, Spoken: str) -> str:
        """Map a spoken name to its written label via the ObjectNames table."""
        try:
            from InputPrompts.NewObjectNameGrammarSwitcher import (
                NewObjectNameGrammarSwitcher,
            )

            NewObjectNameGrammarSwitcher._EnsureDictionaryOnPath()
            from ObjectNames.ObjectNames import ResolveObjectName

            return ResolveObjectName(Spoken, self._Language)
        except Exception:
            return ""

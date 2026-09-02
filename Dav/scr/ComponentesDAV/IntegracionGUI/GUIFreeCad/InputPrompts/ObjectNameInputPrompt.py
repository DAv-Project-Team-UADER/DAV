#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Prompt used to dictate the name of an object being selected."""

from __future__ import annotations

from InputPrompts.StringInputPrompt import StringInputPrompt


class ObjectNameInputPrompt(StringInputPrompt):
    """String prompt that swaps the Vosk grammar to the document's labels.

    Used when picking an existing object by its dictated name: the recognizer
    can only hear a label that is part of the active grammar.

    Naming a *new* object uses plain StringInputPrompt instead — the name does
    not exist in the document yet, so there is nothing to add to the grammar.
    """

    def RequiresObjectNameGrammar(self) -> bool:
        """Return True so the router swaps in the object-label grammar."""
        return True

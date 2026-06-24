#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Common result object returned by DAV input prompts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class PromptResult:
    """Represents the result of a voice-driven input prompt."""

    Success: bool
    Value: Any | None = None
    Cancelled: bool = False
    Error: str = ""

    @classmethod
    def Pending(cls) -> "PromptResult":
        """Build a pending prompt result."""
        return cls(Success=False)

    @classmethod
    def Ok(cls, Value: Any | None = None) -> "PromptResult":
        """Build a successful prompt result."""
        return cls(Success=True, Value=Value)

    @classmethod
    def Cancel(cls) -> "PromptResult":
        """Build a cancelled prompt result."""
        return cls(Success=False, Cancelled=True)

    @classmethod
    def Fail(cls, Error: str) -> "PromptResult":
        """Build a failed prompt result with an error message."""
        return cls(Success=False, Error=Error)

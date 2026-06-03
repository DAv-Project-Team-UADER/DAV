#  Copyright (C) 2026 The DAV Project Team
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Single navigable command in Browser.Context / BaseContext."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class ContextEntry:
    """Maps a spoken phrase to an internal key and executable target."""

    Spoken: str
    InternalKey: str
    Target: Any

    def IsSubContext(self) -> bool:
        return isinstance(self.Target, dict)

    def IsCallable(self) -> bool:
        return callable(self.Target)

    def NormalizeSpoken(self) -> str:
        return " ".join(self.Spoken.lower().split())


def FindBySpoken(entries: list[ContextEntry], spoken: str) -> ContextEntry | None:
    needle = " ".join(spoken.lower().split())
    for entry in entries:
        if entry.NormalizeSpoken() == needle:
            return entry
    return None


def FindByInternalKey(entries: list[ContextEntry], internal_key: str) -> ContextEntry | None:
    key = internal_key.lower()
    for entry in entries:
        if entry.InternalKey.lower() == key:
            return entry
    return None

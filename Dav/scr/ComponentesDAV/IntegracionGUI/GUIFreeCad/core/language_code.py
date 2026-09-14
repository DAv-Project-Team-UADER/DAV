#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Language codes for DAV voice navigation (PascalCase public API)."""

from __future__ import annotations

from enum import Enum


class LanguageCode(Enum):
    """Preference language states (task specification: En, Es, PT)."""

    En = "en"
    Es = "es"
    PT = "pt"

    @classmethod
    def FromStorage(cls, value: str) -> "LanguageCode":
        normalized = (value or "es").strip().lower()
        for item in cls:
            if item.value == normalized:
                return item
        return cls.Es

    @property
    def TranslateModuleSuffix(self) -> str:
        """TraduceTo file stem, e.g. TraduceToEs."""
        if self is LanguageCode.En:
            return "TraduceToEn"
        if self is LanguageCode.PT:
            return "TraduceToPT"
        return "TraduceToEs"

    @property
    def AlternateTranslateSuffixes(self) -> tuple[str, ...]:
        """Fallback stems (some folders use TraduceToPt or TraduceToPtBr)."""
        if self is LanguageCode.PT:
            return ("TraduceToPT", "TraduceToPt", "TraduceToPtBr")
        if self is LanguageCode.En:
            return ("TraduceToEn",)
        return ("TraduceToEs",)

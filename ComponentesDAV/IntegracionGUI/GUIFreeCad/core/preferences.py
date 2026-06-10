#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""DAV preferences facade (SetLanguage public API for Browser)."""

from __future__ import annotations

from typing import Callable

from core.language_code import LanguageCode
from core.settings import settings

LanguageChangeCallback = Callable[[LanguageCode, LanguageCode], None]


class Preferences:
    """
    Public preferences surface used by Browser and the FreeCAD GUI.

    SetLanguage may be En, Es, or PT; changing it notifies registered listeners
    (Browser should reload commands from base.py).
    """

    def __init__(self) -> None:
        self._language_callbacks: list[LanguageChangeCallback] = []
        settings.load()

    @property
    def SetLanguage(self) -> LanguageCode:
        return LanguageCode.FromStorage(settings.language)

    @SetLanguage.setter
    def SetLanguage(self, value: LanguageCode) -> None:
        if not isinstance(value, LanguageCode):
            raise TypeError("SetLanguage must be LanguageCode (En, Es, or PT)")
        previous = self.SetLanguage
        settings.language = value.value
        settings.save()
        if previous is not value:
            for callback in list(self._language_callbacks):
                callback(previous, value)

    def RegisterLanguageChange(self, callback: LanguageChangeCallback) -> None:
        self._language_callbacks.append(callback)

    def UnregisterLanguageChange(self, callback: LanguageChangeCallback) -> None:
        try:
            self._language_callbacks.remove(callback)
        except ValueError:
            pass


preferences = Preferences()

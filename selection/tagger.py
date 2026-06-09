# Copyright (C) 2026 El Equipo del Proyecto DAV
# Copyright (C) 2026 The DAV Project Team
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#
# Este programa se distribuye con la esperanza de que sea útil,
# pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
# MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
# Licencia Pública General GNU para más detalles.
#
# Deberías haber recibido una copia de la Licencia Pública General GNU
# junto con este programa. Si no es así, consulte <http://www.gnu.org/licenses/>.
# SPDX-License-Identifier: GPL-3.0-or-later

"""Language-aware object naming for tacit geometry created by CreateObjects."""

from __future__ import annotations

import sys
from enum import Enum
from pathlib import Path
from typing import Any

try:
    import FreeCAD as App
except ImportError:
    App = None  # type: ignore[assignment,misc]


class LanguageCode(Enum):
    """En, Es, PT — matches GUIFreeCad Preferences.SetLanguage."""

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


_KINDS = ("point", "line", "surface", "edge")

_LABELS: dict[LanguageCode, dict[str, str]] = {
    LanguageCode.En: {
        "point": "Point",
        "line": "Line",
        "surface": "Surface",
        "edge": "Edge",
    },
    LanguageCode.Es: {
        "point": "Punto",
        "line": "Linea",
        "surface": "Superficie",
        "edge": "Arista",
    },
    LanguageCode.PT: {
        "point": "Ponto",
        "line": "Linha",
        "surface": "Superficie",
        "edge": "Aresta",
    },
}


def ResolveLanguage(language: LanguageCode | str | None = None) -> LanguageCode:
    """Return explicit language or read Preferences.SetLanguage from GUIFreeCad."""
    if language is None:
        return _LanguageFromPreferences()
    if isinstance(language, LanguageCode):
        return language
    return LanguageCode.FromStorage(str(language))


def _LanguageFromPreferences() -> LanguageCode:
    import os

    env = os.environ.get("DAV_GUI_FREECAD_ROOT", "").strip()
    if env and Path(env).is_dir():
        candidates = (Path(env),)
    else:
        repo = Path(__file__).resolve().parents[1]
        candidates = (
            repo / "ComponentesDAV" / "IntegracionGUI" / "GUIFreeCad",
            repo / "componentesDAV" / "IntegracionGUI" / "GUIFreeCad",
            repo / "luigiIntegracionV1" / "GUIFreeCad",
            repo / "GUIFreeCad",
        )

    for gui_root in candidates:
        if not gui_root.is_dir():
            continue
        gui_text = str(gui_root)
        if gui_text not in sys.path:
            sys.path.insert(0, gui_text)
        try:
            from core.preferences import preferences

            return preferences.SetLanguage
        except Exception:
            continue

    return LanguageCode.Es


class Tagger:
    """
    Assigns sequential localized names to tacit objects.

    Examples (Es): Punto1, Linea1, Linea2, Superficie3
    Examples (En): Point1, Line1, Surface3
    """

    def __init__(
        self,
        language: LanguageCode | str | None = None,
        document: Any | None = None,
    ) -> None:
        self._language = ResolveLanguage(language)
        self._document = document
        if self._document is None and App is not None:
            self._document = App.ActiveDocument
        self._counters: dict[str, int] = {kind: 0 for kind in _KINDS}

    @property
    def SetLanguage(self) -> LanguageCode:
        return self._language

    @SetLanguage.setter
    def SetLanguage(self, value: LanguageCode | str) -> None:
        self._language = ResolveLanguage(value)

    def NextName(self, kind: str) -> str:
        """Return a unique FreeCAD object Name for the given geometry kind."""
        kind_key = kind.strip().lower()
        if kind_key not in _KINDS:
            raise ValueError(f"Unknown kind '{kind}'. Use: {', '.join(_KINDS)}")

        label = _LABELS[self._language][kind_key]
        while True:
            self._counters[kind_key] += 1
            candidate = f"{label}{self._counters[kind_key]}"
            if self._document is None or self._document.getObject(candidate) is None:
                return candidate

    def FormatLabel(self, kind: str, number: int | None = None) -> str:
        """Human-readable label for the tree view (e.g. 'Superficie 3')."""
        kind_key = kind.strip().lower()
        if kind_key not in _KINDS:
            raise ValueError(f"Unknown kind '{kind}'. Use: {', '.join(_KINDS)}")
        label = _LABELS[self._language][kind_key]
        index = number if number is not None else self._counters[kind_key]
        return f"{label} {index}"

    def ApplyLabel(self, obj: Any, kind: str) -> None:
        """Set obj.Label using the current counter for kind."""
        if obj is None:
            return
        kind_key = kind.strip().lower()
        if hasattr(obj, "Label"):
            obj.Label = self.FormatLabel(kind_key, self._counters[kind_key])

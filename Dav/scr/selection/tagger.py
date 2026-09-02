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

import re
import sys
import unicodedata
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
    def FromStorage(cls, value: Any) -> "LanguageCode":
        if hasattr(value, "value"):
            value = value.value
        val_str = str(value or "es").strip().lower()
        if "en" in val_str:
            return cls.En
        if "pt" in val_str:
            return cls.PT
        return cls.Es


_KINDS = ("point", "line", "surface", "edge", "object")

_LABELS: dict[LanguageCode, dict[str, str]] = {
    LanguageCode.En: {
        "point": "Point",
        "line": "Line",
        "surface": "Surface",
        "edge": "Edge",
        "object": "Object",
    },
    LanguageCode.Es: {
        "point": "Punto",
        "line": "Linea",
        "surface": "Superficie",
        "edge": "Arista",
        "object": "Objeto",
    },
    LanguageCode.PT: {
        "point": "Ponto",
        "line": "Linha",
        "surface": "Superficie",
        "edge": "Aresta",
        "object": "Objeto",
    },
}


def ResolveLanguage(language: Any = None) -> LanguageCode:
    """Return explicit language or read Preferences.SetLanguage from GUIFreeCad."""
    if language is None:
        return _LanguageFromPreferences()
    if type(language) is LanguageCode:
        return language
    return LanguageCode.FromStorage(language)


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

            return LanguageCode.FromStorage(preferences.SetLanguage)
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
        language: LanguageCode | str | Any = None,
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
    def SetLanguage(self, value: LanguageCode | str | Any) -> None:
        self._language = ResolveLanguage(value)

    def _GetLabels(self) -> dict[str, str]:
        lang_str = getattr(self._language, "value", str(self._language)).lower()
        if "en" in lang_str:
            return _LABELS[LanguageCode.En]
        if "pt" in lang_str:
            return _LABELS[LanguageCode.PT]
        return _LABELS[LanguageCode.Es]

    def NextName(self, kind: str) -> str:
        """Return a unique FreeCAD object Name for the given geometry kind."""
        kind_key = kind.strip().lower()
        if kind_key not in _KINDS:
            raise ValueError(f"Unknown kind '{kind}'. Use: {', '.join(_KINDS)}")

        labels = self._GetLabels()
        label = labels[kind_key]
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
        labels = self._GetLabels()
        label = labels[kind_key]
        index = number if number is not None else self._counters[kind_key]
        return f"{label} {index}"

    def ApplyLabel(self, obj: Any, kind: str) -> None:
        """Set obj.Label using the current counter for kind."""
        if obj is None:
            return
        kind_key = kind.strip().lower()
        if hasattr(obj, "Label"):
            obj.Label = self.FormatLabel(kind_key, self._counters[kind_key])

    def ApplyCustomName(self, obj: Any, spoken: str, kind: str = "object") -> str:
        """Rename obj with a user-dictated name, falling back to the counter.

        The spoken text goes to ``obj.Label`` as-is (FreeCAD labels accept
        spaces and accents). ``obj.Name`` is read-only once the object exists,
        so only the Label carries the dictated name; lookups by voice go
        through ObjectSelection.SelectByLabel.

        Args:
            obj: FreeCAD object to rename.
            spoken: Raw text dictated by the user; may be empty.
            kind: Tagger kind used for the automatic fallback name.

        Returns:
            The label actually applied.

        Example::

            Tagger().ApplyCustomName(box, "mesa")  # -> "mesa"
        """
        if obj is None:
            return ""

        label = self.SanitizeSpokenName(spoken)
        if not label:
            # Sin dictado valido se cae al nombre automatico (Objeto 1, Objeto 2...)
            self._counters[kind] = self._counters.get(kind, 0) + 1
            label = self.FormatLabel(kind, self._counters[kind])

        label = self._UniqueLabel(label, obj)
        if hasattr(obj, "Label"):
            obj.Label = label
        return label

    def _UniqueLabel(self, label: str, obj: Any = None) -> str:
        """Append a numeric suffix while another object already uses the label.

        ``obj`` itself is excluded from the check: FreeCAD copies the base
        object's Label into a derived one (an extrusion of "Mesa" is born
        named "Mesa"), and without this the object would be renamed away from
        the very name being applied to it — "Mesa" turning into "Mesa 2".
        """
        if self._document is None:
            return label

        existing = {
            getattr(other, "Label", "")
            for other in getattr(self._document, "Objects", [])
            if other is not obj
        }
        if label not in existing:
            return label

        index = 2
        while f"{label} {index}" in existing:
            index += 1
        return f"{label} {index}"

    @staticmethod
    def SanitizeSpokenName(spoken: str) -> str:
        """Clean dictated text into a usable FreeCAD label.

        Collapses whitespace and drops characters FreeCAD rejects in labels.
        Accents are kept: the label is what the user reads in the tree.
        """
        if not spoken:
            return ""
        cleaned = re.sub(r"[^\w\s-]", "", spoken, flags=re.UNICODE)
        return re.sub(r"\s+", " ", cleaned).strip()

    @staticmethod
    def NormalizeForMatch(text: str) -> str:
        """Fold text for lenient voice matching (no accents, no case, no spaces)."""
        if not text:
            return ""
        folded = (
            unicodedata.normalize("NFKD", text)
            .encode("ASCII", "ignore")
            .decode()
            .lower()
        )
        return re.sub(r"[^a-z0-9]", "", folded)

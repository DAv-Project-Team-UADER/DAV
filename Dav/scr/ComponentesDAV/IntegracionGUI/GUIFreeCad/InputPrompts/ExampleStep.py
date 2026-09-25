#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""One frame of a guided example and the navigation words shared by its prompts."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

# Palabras de navegación por idioma. Las usan el selector de ejemplos y el
# reproductor; ambos aceptan las de los tres idiomas a la vez.
NAVIGATION_WORDS: dict[str, dict[str, tuple[str, ...]]] = {
    "es": {
        "previous": ("retroceder",),
        "next": ("avanzar",),
        "select": ("enviar",),
        "skip": ("saltar",),
    },
    "en": {
        "previous": ("back",),
        "next": ("next",),
        "select": ("send",),
        "skip": ("skip",),
    },
    "pt": {
        "previous": ("voltar",),
        "next": ("próximo",),
        "select": ("enviar",),
        "skip": ("pular",),
    },
}

# Sinónimos que el reproductor da por buenos: palabra oída (sin tildes) -> palabra esperada.
WORD_SYNONYMS: dict[str, str] = {
    "coma": "punto",
}

_DEFAULT_LANGUAGE = "es"


def _Pick(Table: Any, Language: str) -> Any:
    """Return ``Table[Language]`` falling back to Spanish; ``None`` when absent."""
    if not isinstance(Table, dict):
        return Table
    return Table.get(Language, Table.get(_DEFAULT_LANGUAGE))


@dataclass(frozen=True, eq=False)
class ExampleStep:
    """A frame: what to show, what to say to do it in DAV, and what to run."""

    Text: dict[str, str]
    Path: dict[str, tuple[str, ...]]
    Action: Callable[[], None]
    Values: Any = None

    def GetText(self, Language: str) -> str:
        """Return the instruction in ``Language`` (Spanish if missing)."""
        return _Pick(self.Text, Language) or ""

    def GetPath(self, Language: str) -> tuple[str, ...]:
        """Return the command-tree phrases in ``Language`` (Spanish if missing)."""
        return tuple(_Pick(self.Path, Language) or ())

    def GetValues(self, Language: str) -> tuple[str, ...]:
        """Return the words dictated in the command dialogs.

        ``Values`` may be a per-language dict or a function ``f(language)``
        evaluated on every call, since it can depend on the document.
        """
        values = self.Values
        if values is None:
            return ()
        if callable(values):
            return tuple(values(Language))
        return tuple(_Pick(values, Language) or ())

    def GetSay(self, Language: str) -> tuple[str, ...]:
        """Return everything to say, in order: path first, then values."""
        return self.GetPath(Language) + self.GetValues(Language)

#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Find the object whose name looks most like a spelled one ("buscar por deletreo").

El reconocedor de voz se equivoca justo en las letras que suenan parecido (be, de,
pe, te, ve...), así que no alcanza con comparar texto exacto: se ordenan los objetos
por parecido, y se cuentan como errores chicos las confusiones de letras vecinas.
"""

from __future__ import annotations

import unicodedata
from typing import Sequence

# Letras que el reconocedor confunde entre sí: sus nombres riman («be», «de», «pe»...
# terminan en «e»; «efe», «ele», «eme»... empiezan con «e»). Cambiar una por otra
# cuesta la mitad que cambiarla por una letra cualquiera.
_CONFUSABLE_GROUPS = ("bcdgptvz", "flmnrsx", "iy", "kq", "ou")
_CONFUSABLE = {
    (a, b)
    for group in _CONFUSABLE_GROUPS
    for a in group
    for b in group
    if a != b
}
_CONFUSABLE_COST = 0.5

# Cuando lo deletreado es el comienzo del nombre («tri» para «Triangle»), el parecido
# con ese comienzo vale un poco menos que el de un nombre completo igual.
_PREFIX_FACTOR = 0.92


def Normalize(Text: str) -> str:
    """Return ``Text`` lower case, without accents and keeping only letters and digits.

    «Hoja A», «hoja_a» y «HOJAA» quedan iguales, que es como se deletrean.

    Example::

        Normalize("Tijera Ábierta_01")   # 'tijeraabierta01'
    """
    decomposed = unicodedata.normalize("NFD", Text.lower())
    stripped = "".join(char for char in decomposed if unicodedata.category(char) != "Mn")
    return "".join(char for char in stripped if char.isalnum())


def _SubstitutionCost(First: str, Second: str) -> float:
    if First == Second:
        return 0.0
    if (First, Second) in _CONFUSABLE:
        return _CONFUSABLE_COST
    return 1.0


def _Distance(First: str, Second: str) -> float:
    """Levenshtein distance where swapping confusable letters costs less."""
    previous = [float(index) for index in range(len(Second) + 1)]
    for row, char_a in enumerate(First, start=1):
        current = [float(row)]
        for column, char_b in enumerate(Second, start=1):
            current.append(
                min(
                    previous[column] + 1.0,
                    current[column - 1] + 1.0,
                    previous[column - 1] + _SubstitutionCost(char_a, char_b),
                )
            )
        previous = current
    return previous[-1]


def _Similarity(First: str, Second: str) -> float:
    longest = max(len(First), len(Second))
    if longest == 0:
        return 0.0
    return 1.0 - _Distance(First, Second) / longest


def Score(Query: str, Name: str) -> float:
    """Return how much ``Name`` looks like ``Query``, from 0 (nothing) to 1 (identical).

    Args:
        Query: What the user spelled.
        Name: A name or label of an object.

    Example::

        Score("TRIANGUL", "Triangle001")   # alto: es casi su comienzo
    """
    query, name = Normalize(Query), Normalize(Name)
    if not query or not name:
        return 0.0
    best = _Similarity(query, name)
    if len(query) < len(name):
        best = max(best, _PREFIX_FACTOR * _Similarity(query, name[: len(query)]))
    return best


def RankMatches(
    Query: str,
    Candidates: Sequence[Sequence[str]],
    Limit: int = 5,
    MinScore: float = 0.45,
) -> list[tuple[int, float]]:
    """Order candidates by how much they look like what was spelled.

    Args:
        Query: The spelled text.
        Candidates: One entry per object, with every name it can be called by
            (for example ``(Name, Label)``). The best of them counts.
        Limit: Maximum number of results.
        MinScore: Candidates scoring below this are left out.

    Returns:
        ``(index in Candidates, score)`` pairs, best first.

    Example::

        RankMatches("HOJA A", [("Body", "Hoja A"), ("Body001", "Hoja B")])
        # [(0, 1.0), (1, 0.8...)]
    """
    ranked = []
    for index, names in enumerate(Candidates):
        score = max((Score(Query, name) for name in names if name), default=0.0)
        if score >= MinScore:
            ranked.append((index, score))
    # a igual parecido gana el que está antes en la lista
    ranked.sort(key=lambda pair: (-pair[1], pair[0]))
    return ranked[:Limit]

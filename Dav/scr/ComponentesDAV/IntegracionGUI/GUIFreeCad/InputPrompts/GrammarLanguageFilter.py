#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Keep out of a Vosk grammar the words that belong to another language.

The prompts accept confirm/cancel words in the three languages at once, so
that saying "ok" works with a Spanish interface. The *grammar* must not do
the same: a word the loaded model does not know cannot ever be recognised,
but it still competes for the audio and crowds out the words that are valid.

Observed with the Spanish model: "accept", "send" and "enter" were pushed
into the grammar alongside "aceptar" and "enviar", and only those two ever
matched — "confirmar" and "entrar" stopped working.

The lists come from NavCommands/TraduceTo*.py, so a synonym added there is
classified automatically without touching this file.
"""

from __future__ import annotations

import functools


@functools.lru_cache(maxsize=8)
def _WordsForLanguage(language: str) -> frozenset[str]:
    """Return the confirm/cancel words declared for one language.

    Args:
        language: Two-letter code ('es', 'en', 'pt').

    Returns:
        The spoken words from that language's NavCommands table. Empty when
        the dictionary cannot be read, which callers treat as "allow all".
    """
    module_name = {
        "en": "TraduceToEn",
        "pt": "TraduceToPT",
    }.get(language, "TraduceToEs")

    try:
        import importlib
        import sys

        from integration.voice_bootstrap import _resolve_dictionary_root

        root = _resolve_dictionary_root()
        parent = str(root.parent)
        if parent not in sys.path:
            sys.path.insert(0, parent)

        package = root.name
        actions = importlib.import_module(
            f"{package}.NavCommands.NavActions"
        ).NavActions
        send, cancel = actions.get("send"), actions.get("cancel")

        module = importlib.import_module(
            f"{package}.NavCommands.{module_name}"
        )
        mapping = getattr(module, module_name, {})
    except Exception:
        return frozenset()

    return frozenset(
        spoken.strip().lower()
        for spoken, target in mapping.items()
        if target is send or target is cancel
    )


def BelongsToLanguage(word: str, language: str = "es") -> bool:
    """Return True when the word may enter the grammar for this language.

    Falls back to allowing everything when the dictionary is unreadable: a
    grammar with extra words still works, one with none does not.

    Example::

        BelongsToLanguage("aceptar", "es")  # True
        BelongsToLanguage("accept", "es")   # False
    """
    code = str(language or "es").strip().lower()[:2]
    allowed = _WordsForLanguage(code)
    if not allowed:
        return True
    return word.strip().lower() in allowed

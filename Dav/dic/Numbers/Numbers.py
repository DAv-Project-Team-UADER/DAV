# Copyright (C) 2026 El Equipo del Proyecto DAV
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

"""Numeric sentinel actions and grammar builder for Vosk numeric input."""


def Zero() -> None:
    """Sentinel: digit zero."""
    return None


def One() -> None:
    """Sentinel: digit one."""
    return None


def Two() -> None:
    """Sentinel: digit two."""
    return None


def Three() -> None:
    """Sentinel: digit three."""
    return None


def Four() -> None:
    """Sentinel: digit four."""
    return None


def Five() -> None:
    """Sentinel: digit five."""
    return None


def Six() -> None:
    """Sentinel: digit six."""
    return None


def Seven() -> None:
    """Sentinel: digit seven."""
    return None


def Eight() -> None:
    """Sentinel: digit eight."""
    return None


def Nine() -> None:
    """Sentinel: digit nine."""
    return None


def DecimalPoint() -> None:
    """Sentinel: decimal point separator."""
    return None


def DecimalComma() -> None:
    """Sentinel: decimal comma separator."""
    return None


def CompoundNumber() -> None:
    """Sentinel: any spoken number word beyond a single digit.

    Covers 10-19, the tens (20-90), and the Spanish 21-29 contractions
    ("veintidos"). A single shared sentinel is enough for all of them:
    get_numeric_grammar_phrases only reads the *keys* of TraduceTo*.py to
    build the Vosk grammar, the value's identity is never dispatched, so a
    sentinel per number would only add boilerplate. The actual value is
    computed by SpokenNumberParser from the word itself.
    """
    return None


Numbers = {
    "zero":     Zero,
    "one":      One,
    "two":      Two,
    "three":    Three,
    "four":     Four,
    "five":     Five,
    "six":      Six,
    "seven":    Seven,
    "eight":    Eight,
    "nine":     Nine,
    "point":    DecimalPoint,
    "comma":    DecimalComma,
    "compound": CompoundNumber,
}


# Idioma -> modulo de traduccion, en Numbers/ y en NavCommands/ (este ultimo
# usa el sufijo "PT" en mayusculas, a diferencia de Numbers que usa "Pt").
_NUMBER_MODULE_BY_LANGUAGE = {"es": "TraduceToEs", "en": "TraduceToEn", "pt": "TraduceToPt"}
_NAV_MODULE_BY_LANGUAGE = {"es": "TraduceToEs", "en": "TraduceToEn", "pt": "TraduceToPT"}

# Respaldo minimo por idioma si NavCommands no esta disponible, para que un
# diccionario roto no deje los prompts numericos sin poder confirmar/cancelar.
_FALLBACK_CONFIRMATION_WORDS = {
    "es": {"enviar", "aceptar", "confirmar", "entrar", "ok"},
    "en": {"send", "enter", "accept", "confirm", "ok"},
    "pt": {"enviar", "aceitar", "confirmar", "entrar", "ok"},
}
_FALLBACK_CANCELLATION_WORDS = {
    "es": {"cancelar", "cancela"},
    "en": {"cancel"},
    "pt": {"cancelar", "cancelamento"},
}


def get_numeric_grammar_phrases(language: str = "es") -> list[str]:
    """Build the Vosk grammar phrase list for numeric input in `language`.

    Returns only the digit/decimal words, confirmation words and
    cancellation words for the given language ("es"/"en"/"pt"), plus [unk].
    Restricting the grammar to a single language keeps Vosk from accepting
    numbers spoken in a language other than the one currently configured.

    Args:
        language: Configured DAV language ("es", "en" or "pt"). Unknown
            values fall back to "es".
    """
    import sys
    from pathlib import Path

    if language not in _NUMBER_MODULE_BY_LANGUAGE:
        language = "es"

    phrases: set[str] = set()

    # Dav/dic/ must be in sys.path for the relative imports in
    # TraduceTo*.py (from .Numbers import Numbers) to work.
    dic_root = str(Path(__file__).resolve().parent.parent)
    if dic_root not in sys.path:
        sys.path.insert(0, dic_root)

    lang_name = _NUMBER_MODULE_BY_LANGUAGE[language]
    try:
        import importlib
        module = importlib.import_module(f"Numbers.{lang_name}")
        mapping = getattr(module, lang_name, {})
        for spoken in mapping.keys():
            if spoken:
                phrases.add(spoken.strip().lower())
    except Exception:
        pass

    # Confirmation and cancellation words for this language, so the user can
    # say "enviar" / "cancelar" while in a numeric prompt. Sourced from
    # NavCommands/TraduceTo*.py (the app's single source of truth for these
    # words) instead of a second hardcoded list.
    phrases.update(
        _GetNavWords(language, "send") or _FALLBACK_CONFIRMATION_WORDS[language]
    )
    phrases.update(
        _GetNavWords(language, "cancel") or _FALLBACK_CANCELLATION_WORDS[language]
    )

    phrases.add("[unk]")
    return sorted(phrases)


def _GetNavWords(language: str, action: str) -> set[str] | None:
    """Spoken words for a NavActions entry ("send"/"cancel") in `language`.

    Returns None (instead of an empty set) when NavCommands can't be
    imported, so callers can tell "not available" apart from "no synonyms
    defined" and fall back to the built-in word list.
    """
    try:
        import importlib

        nav_module = _NAV_MODULE_BY_LANGUAGE[language]
        actions = importlib.import_module("NavCommands.NavActions").NavActions
        target = actions.get(action)
        module = importlib.import_module(f"NavCommands.{nav_module}")
        mapping = getattr(module, nav_module, {})
        return {
            spoken.strip().lower() for spoken, value in mapping.items() if value is target
        }
    except Exception:
        return None

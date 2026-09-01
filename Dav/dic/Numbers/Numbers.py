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


Numbers = {
    "zero":   Zero,
    "one":    One,
    "two":    Two,
    "three":  Three,
    "four":   Four,
    "five":   Five,
    "six":    Six,
    "seven":  Seven,
    "eight":  Eight,
    "nine":   Nine,
    "point":  DecimalPoint,
    "comma":  DecimalComma,
}


def get_numeric_grammar_phrases() -> list[str]:
    """Build the full phrase list for Vosk grammar during numeric input.

    Returns a list containing all number words from es/en/pt translations,
    confirmation/cancellation words, and [unk].
    This list is used to replace the CAD grammar while a numeric prompt
    is active, so Vosk can recognize spoken digits and decimal separators.
    """
    import sys
    from pathlib import Path

    phrases: set[str] = set()

    # Number words from all three language translations.
    # Dav/dic/ must be in sys.path for the relative imports in
    # TraduceTo*.py (from .Numbers import Numbers) to work.
    dic_root = str(Path(__file__).resolve().parent.parent)
    if dic_root not in sys.path:
        sys.path.insert(0, dic_root)

    for lang_name in ("TraduceToEs", "TraduceToEn", "TraduceToPt"):
        try:
            import importlib
            module = importlib.import_module(f"Numbers.{lang_name}")
            mapping = getattr(module, lang_name, {})
            for spoken in mapping.keys():
                if spoken:
                    phrases.add(spoken.strip().lower())
        except Exception:
            pass

    # Confirmation and cancellation words, so the user can say "enviar" /
    # "cancelar" while in a numeric prompt.
    phrases |= {
        "enviar", "aceptar", "confirmar", "entrar", "ok",
        "send", "enter", "accept", "confirm",
        "cancelar", "cancel", "cancela",
    }

    phrases.add("[unk]")
    return sorted(phrases)

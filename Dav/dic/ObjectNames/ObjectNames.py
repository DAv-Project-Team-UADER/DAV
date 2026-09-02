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

"""Vocabulary of names that can be dictated when naming a new object.

Vosk can only transcribe words that are in its active grammar, so naming an
object by voice needs a closed list: free text is not recognizable. These are
the words offered when the "name this object" prompt opens.

The words themselves live in TraduceTo*.py like any other DAV dictionary, so
the team can add a name without touching Python code.
"""


def GetObjectNamePhrases(language: str = "es") -> list[str]:
    """Return the dictatable object names for the given language.

    Args:
        language: Two-letter code ('es', 'en', 'pt'). Unknown values fall
            back to Spanish.

    Returns:
        Sorted spoken names, ready to be handed to Vosk as a grammar.

    Example::

        GetObjectNamePhrases("es")  # -> ['aro', 'base', 'brida', ...]
    """
    table = _LoadTable(language)
    return sorted(table)


def ResolveObjectName(spoken: str, language: str = "es") -> str:
    """Return the canonical written form of a dictated name.

    Lets the spoken form differ from what is written in the tree (e.g. a
    recognizer-friendly synonym mapping to a nicer label).

    Args:
        spoken: What the recognizer heard.
        language: Two-letter language code.

    Returns:
        The label to write, or '' when the phrase is not a known name.
    """
    if not spoken:
        return ""
    table = _LoadTable(language)
    return table.get(spoken.strip().lower(), "")


def _LoadTable(language: str) -> dict[str, str]:
    """Import the TraduceTo* table for the language, or {} if unavailable."""
    code = str(language or "es").strip().lower()[:2]
    module_name = {
        "en": "TraduceToEn",
        "pt": "TraduceToPT",
    }.get(code, "TraduceToEs")

    try:
        module = __import__(
            f"ObjectNames.{module_name}", fromlist=[module_name]
        )
    except Exception:
        return {}

    table = getattr(module, module_name, None)
    return dict(table) if isinstance(table, dict) else {}

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

"""Words the user dictates inside the dialogs of a command: numbers, send, down, next."""

# Números que usan los ejemplos, dichos como los reconoce el modelo de Vosk.
_NUMBERS = {
    "es": {
        0: "cero", 1: "uno", 2: "dos", 3: "tres", 4: "cuatro", 5: "cinco", 6: "seis", 8: "ocho",
        10: "diez", 12: "doce", 16: "dieciséis", 20: "veinte", 22: "veintidós", 24: "veinticuatro",
        30: "treinta", 40: "cuarenta", 60: "sesenta",
    },
    "en": {
        0: "zero", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 8: "eight",
        10: "ten", 12: "twelve", 16: "sixteen", 20: "twenty", 22: "twenty two", 24: "twenty four",
        30: "thirty", 40: "forty", 60: "sixty",
    },
    "pt": {
        0: "zero", 1: "um", 2: "dois", 3: "três", 4: "quatro", 5: "cinco", 6: "seis", 8: "oito",
        10: "dez", 12: "doze", 16: "dezesseis", 20: "vinte", 22: "vinte e dois", 24: "vinte e quatro",
        30: "trinta", 40: "quarenta", 60: "sessenta",
    },
}

_MINUS = {"es": "menos", "en": "minus", "pt": "menos"}
_SEND = {"es": "enviar", "en": "send", "pt": "enviar"}
_DOWN = {"es": "abajo", "en": "down", "pt": "abaixo"}
_NEXT = {"es": "avanzar", "en": "next", "pt": "avancar"}
_NO = {"es": "no", "en": "no", "pt": "nao"}
_POINT = {"es": "coma", "en": "point", "pt": "virgula"}


def _lang(language: str) -> str:
    return language if language in _SEND else "es"


def send(language: str) -> tuple[str, ...]:
    """The word that confirms a dialog («enviar»)."""
    return (_SEND[_lang(language)],)


def no(language: str) -> tuple[str, ...]:
    """The answer «no» to a yes/no question."""
    return (_NO[_lang(language)],)


def down(language: str, times: int) -> tuple[str, ...]:
    """The word that moves down a list, repeated ``times`` times."""
    return (_DOWN[_lang(language)],) * times


def nextItem(language: str, times: int) -> tuple[str, ...]:
    """The word that moves to the next object of a list, repeated ``times`` times."""
    return (_NEXT[_lang(language)],) * times


def numbers(language: str, *values: int) -> tuple[str, ...]:
    """Dictate each value followed by «enviar», the way each parameter is asked.

    Args:
        language: ``"es"``, ``"en"`` or ``"pt"``.
        *values: integers to dictate; a negative one is said with «menos».

    Returns:
        The words, e.g. ``numbers("es", 0, -5)`` gives
        ``("cero", "enviar", "menos", "cinco", "enviar")``.
    """
    lang = _lang(language)
    words: list[str] = []
    for value in values:
        if value < 0:
            words.append(_MINUS[lang])
        words.append(_NUMBERS[lang][abs(value)])
        words.append(_SEND[lang])
    return tuple(words)


def decimal(language: str, whole: int, fraction: int) -> tuple[str, ...]:
    """Dictate a one-digit decimal followed by «enviar», e.g. 0.5 as «cero coma cinco enviar».

    Args:
        language: ``"es"``, ``"en"`` or ``"pt"``.
        whole: the integer part.
        fraction: the digit after the decimal point.
    """
    lang = _lang(language)
    return (
        _NUMBERS[lang][whole],
        _POINT[lang],
        _NUMBERS[lang][fraction],
        _SEND[lang],
    )

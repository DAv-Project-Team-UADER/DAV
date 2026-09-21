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

from decimal import Decimal

# Los números del 0 al 19 y las decenas, dichos como los reconoce el modelo de Vosk.
_UNITS = {
    "es": (
        "cero", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve",
        "diez", "once", "doce", "trece", "catorce", "quince", "dieciséis", "diecisiete",
        "dieciocho", "diecinueve",
    ),
    "en": (
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
        "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen",
        "eighteen", "nineteen",
    ),
    "pt": (
        "zero", "um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove",
        "dez", "onze", "doze", "treze", "catorze", "quinze", "dezesseis", "dezessete",
        "dezoito", "dezenove",
    ),
}
# 20, 30, ... 90
_TENS = {
    "es": ("veinte", "treinta", "cuarenta", "cincuenta", "sesenta", "setenta", "ochenta", "noventa"),
    "en": ("twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"),
    "pt": ("vinte", "trinta", "quarenta", "cinquenta", "sessenta", "setenta", "oitenta", "noventa"),
}
# en español del 21 al 29 se dicen en una sola palabra
_TWENTIES_ES = (
    "veintiuno", "veintidós", "veintitrés", "veinticuatro", "veinticinco", "veintiséis",
    "veintisiete", "veintiocho", "veintinueve",
)
# lo que une decena y unidad: «treinta y dos», «twenty two», «trinta e dois»
_JOIN = {"es": ("y",), "en": (), "pt": ("e",)}

_MINUS = {"es": "menos", "en": "minus", "pt": "menos"}
_SEND = {"es": "enviar", "en": "send", "pt": "enviar"}
_DOWN = {"es": "abajo", "en": "down", "pt": "abaixo"}
_NEXT = {"es": "avanzar", "en": "next", "pt": "avancar"}
_NO = {"es": "no", "en": "no", "pt": "nao"}
_YES = {"es": "si", "en": "yes", "pt": "sim"}
# la palabra del decimal es «punto» en los tres idiomas; en español también se acepta «coma»
# (el reproductor de ejemplos lo sabe: ver WORD_SYNONYMS en InputPrompts/ExampleStep.py)
_POINT = {"es": "punto", "en": "point", "pt": "ponto"}


def _lang(language: str) -> str:
    return language if language in _SEND else "es"


def send(language: str) -> tuple[str, ...]:
    """The word that confirms a dialog («enviar»)."""
    return (_SEND[_lang(language)],)


def no(language: str) -> tuple[str, ...]:
    """The answer «no» to a yes/no question."""
    return (_NO[_lang(language)],)


def yes(language: str) -> tuple[str, ...]:
    """The answer «sí» to a yes/no question."""
    return (_YES[_lang(language)],)


def down(language: str, times: int) -> tuple[str, ...]:
    """The word that moves down a list, repeated ``times`` times."""
    return (_DOWN[_lang(language)],) * times


def nextItem(language: str, times: int) -> tuple[str, ...]:
    """The word that moves to the next object of a list, repeated ``times`` times."""
    return (_NEXT[_lang(language)],) * times


def _integerWords(lang: str, value: int) -> list[str]:
    """Say a whole number: the natural word up to 99, digit by digit from 100 on."""
    units = _UNITS[lang]
    if value < 20:
        return [units[value]]
    if value < 100:
        tens, unit = divmod(value, 10)
        if unit == 0:
            return [_TENS[lang][tens - 2]]
        if lang == "es" and tens == 2:
            return [_TWENTIES_ES[unit - 1]]
        return [_TENS[lang][tens - 2], *_JOIN[lang], units[unit]]
    # «uno cero cero» es 100: el parser junta los dígitos
    return [units[int(digit)] for digit in str(value)]


def numbers(language: str, *values: float) -> tuple[str, ...]:
    """Dictate each value followed by «enviar», the way each parameter is asked.

    Whole numbers up to 99 are said naturally («treinta y dos»); from 100 on they are
    spelled digit by digit. A decimal is said with «punto» and its digits one by one.

    Args:
        language: ``"es"``, ``"en"`` or ``"pt"``.
        *values: numbers to dictate, whole or decimal; a negative one is said with «menos».

    Returns:
        The words, e.g. ``numbers("es", 0, -5)`` gives
        ``("cero", "enviar", "menos", "cinco", "enviar")`` and ``numbers("es", 1.11)`` gives
        ``("uno", "punto", "uno", "uno", "enviar")``.

    Example::

        numbers("en", 12.5)  # ("twelve", "point", "five", "send")
    """
    lang = _lang(language)
    words: list[str] = []
    for value in values:
        # Decimal(str(...)) evita que 6.4 salga como 6.4000000000000004
        text = format(Decimal(str(value)).normalize(), "f")
        if text.startswith("-"):
            words.append(_MINUS[lang])
            text = text[1:]
        whole, _, fraction = text.partition(".")
        words += _integerWords(lang, int(whole))
        if fraction:
            words.append(_POINT[lang])
            words += [_UNITS[lang][int(digit)] for digit in fraction]
        words.append(_SEND[lang])
    return tuple(words)

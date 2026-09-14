#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Parse spoken numeric phrases into integer and float values."""

from __future__ import annotations

import re
import unicodedata


class SpokenNumberParser:
    """Converts voice-recognized numeric phrases into Python numbers."""

    DigitWords: dict[str, str] = {
        "cero": "0",
        "zero": "0",
        "uno": "1",
        "un": "1",
        "una": "1",
        "one": "1",
        "um": "1",
        "uma": "1",
        "dos": "2",
        "two": "2",
        "dois": "2",
        "duas": "2",
        "tres": "3",
        "three": "3",
        "cuatro": "4",
        "four": "4",
        "quatro": "4",
        "cinco": "5",
        "five": "5",
        "seis": "6",
        "six": "6",
        "meia": "6",
        "siete": "7",
        "seven": "7",
        "sete": "7",
        "ocho": "8",
        "eight": "8",
        "oito": "8",
        "nueve": "9",
        "nine": "9",
        "nove": "9",
        # 10-19: numeros de una sola palabra, no se arman por concatenacion.
        "diez": "10",
        "ten": "10",
        "dez": "10",
        "once": "11",
        "eleven": "11",
        "onze": "11",
        "doce": "12",
        "twelve": "12",
        "doze": "12",
        "trece": "13",
        "thirteen": "13",
        "treze": "13",
        "catorce": "14",
        "fourteen": "14",
        "catorze": "14",
        "quatorze": "14",
        "quince": "15",
        "fifteen": "15",
        "quinze": "15",
        "dieciseis": "16",
        "sixteen": "16",
        "dezesseis": "16",
        "diecisiete": "17",
        "seventeen": "17",
        "dezessete": "17",
        "dieciocho": "18",
        "eighteen": "18",
        "dezoito": "18",
        "diecinueve": "19",
        "nineteen": "19",
        "dezenove": "19",
        # Decenas (20-90) dichas solas, sin unidad detras ("treinta" -> 30).
        "veinte": "20",
        "twenty": "20",
        "vinte": "20",
        "treinta": "30",
        "thirty": "30",
        "trinta": "30",
        "cuarenta": "40",
        "forty": "40",
        "quarenta": "40",
        "cincuenta": "50",
        "fifty": "50",
        "cinquenta": "50",
        "sesenta": "60",
        "sixty": "60",
        "sessenta": "60",
        "setenta": "70",
        "seventy": "70",
        "ochenta": "80",
        "eighty": "80",
        "oitenta": "80",
        "noventa": "90",
        "ninety": "90",
        # 21-29 contraidos en español ("veintidos"), unica lengua de las tres
        # que los dice como una sola palabra en vez de "veinte y dos".
        "veintiuno": "21",
        "veintidos": "22",
        "veintitres": "23",
        "veinticuatro": "24",
        "veinticinco": "25",
        "veintiseis": "26",
        "veintisiete": "27",
        "veintiocho": "28",
        "veintinueve": "29",
    }

    # Palabras de decena (20-90) que se combinan con una unidad siguiente
    # ("treinta y dos" -> 32, "twenty two" -> 22, "vinte e um" -> 21). Se
    # necesitan como valores enteros aparte de DigitWords porque hay que
    # sumarlas con la unidad, no solo reconocerlas como palabra suelta.
    TensWords: dict[str, int] = {
        "veinte": 20,
        "twenty": 20,
        "vinte": 20,
        "treinta": 30,
        "thirty": 30,
        "trinta": 30,
        "cuarenta": 40,
        "forty": 40,
        "quarenta": 40,
        "cincuenta": 50,
        "fifty": 50,
        "cinquenta": 50,
        "sesenta": 60,
        "sixty": 60,
        "sessenta": 60,
        "setenta": 70,
        "seventy": 70,
        "ochenta": 80,
        "eighty": 80,
        "oitenta": 80,
        "noventa": 90,
        "ninety": 90,
    }

    # Conector opcional entre decena y unidad. El ingles no usa uno en este
    # rango ("twenty two"), por eso no aparece aca.
    ConnectorWords: set[str] = {"y", "e"}

    # Unidades 1-9 con valor entero, derivadas de DigitWords para no repetir
    # la lista: se usan solo para sumarlas a una decena en _MergeTensAndUnits.
    UnitWords: dict[str, int] = {
        word: int(value)
        for word, value in DigitWords.items()
        if value.isdigit() and 1 <= int(value) <= 9
    }

    DecimalWords: set[str] = {
        "coma",
        "punto",
        "decimal",
        "comma",
        "point",
        "virgula",
        "ponto",
    }
    NegativeWords: set[str] = {"menos", "minus", "negative", "negativo"}

    # Estas dos se completan al final del modulo con lo que haya en
    # Dav/dic/NavCommands/TraduceTo*.py, para que sumar un sinonimo sea editar
    # el diccionario y no tres archivos de codigo. Lo que queda escrito aca es
    # el respaldo por si el diccionario no se puede cargar.
    #
    # A diferencia del Browser, que trabaja en un idioma por vez, los prompts
    # aceptan los tres a la vez: el usuario puede decir "ok" con la interfaz en
    # espanol y tiene que andar igual.
    ConfirmationWords: set[str] = {
        "enter",
        "entrar",
        "enviar",
        "send",
        "ok",
        "okey",
        "okay",
        "aceptar",
        "aceitar",
        "confirmar",
        "accept",
        "confirm",
        "listo",
        "vale",
        "hecho",
        "dale",
        "si",
        "bueno",
        "done",
        "yes",
        "yep",
        "pronto",
        "feito",
        "sim",
    }
    CancellationWords: set[str] = {
        "cancelar",
        "cancel",
        "cancela",
        "cancelamento",
        "descartar",
        "discard",
        "anular",
        "abortar",
        "abort",
        "no",
        "nao",
        "olvidalo",
        "never mind",
    }

    @classmethod
    def ParseInteger(cls, Phrase: str) -> int:
        """Parse a spoken phrase into an integer."""
        number_text = cls.ParseNumberText(Phrase, AllowDecimal=False)
        return int(number_text)

    @classmethod
    def ParseFloat(cls, Phrase: str) -> float:
        """Parse a spoken phrase into a float."""
        number_text = cls.ParseNumberText(Phrase, AllowDecimal=True)
        return float(number_text)

    @classmethod
    def TryParseInteger(cls, Phrase: str) -> int | None:
        """Return an integer when parsing succeeds, otherwise None."""
        try:
            return cls.ParseInteger(Phrase)
        except ValueError:
            return None

    @classmethod
    def TryParseFloat(cls, Phrase: str) -> float | None:
        """Return a float when parsing succeeds, otherwise None."""
        try:
            return cls.ParseFloat(Phrase)
        except ValueError:
            return None

    @classmethod
    def ParseNumberText(cls, Phrase: str, *, AllowDecimal: bool) -> str:
        """Convert a spoken phrase into a numeric string."""
        tokens = cls.Tokenize(Phrase)
        if not tokens:
            raise ValueError("No numeric phrase was provided.")
        tokens = cls._MergeTensAndUnits(tokens)

        sign = ""
        digits: list[str] = []
        decimal_seen = False
        digit_seen = False

        for token in tokens:
            if token in cls.ConfirmationWords:
                break
            if token in cls.CancellationWords:
                raise ValueError("Numeric input was cancelled.")
            if token in cls.NegativeWords and not digit_seen and not sign:
                sign = "-"
                continue
            if token in cls.DecimalWords:
                if not AllowDecimal:
                    raise ValueError("Decimal separator is not valid for integer input.")
                if decimal_seen:
                    raise ValueError("Multiple decimal separators were provided.")
                digits.append(".")
                decimal_seen = True
                continue

            numeric_token = cls._TokenToNumericText(token)
            if numeric_token is None:
                continue

            if "." in numeric_token:
                if not AllowDecimal:
                    raise ValueError("Decimal number is not valid for integer input.")
                if decimal_seen:
                    raise ValueError("Multiple decimal separators were provided.")
                whole, decimal = numeric_token.split(".", 1)
                if whole:
                    digits.append(whole)
                    digit_seen = True
                digits.append(".")
                decimal_seen = True
                if decimal:
                    digits.append(decimal)
                    digit_seen = True
                continue

            digits.append(numeric_token)
            digit_seen = True

        if not digit_seen:
            raise ValueError(f"No numeric value could be parsed from: {Phrase!r}")

        number_text = sign + "".join(digits)
        if number_text.endswith("."):
            number_text += "0"
        if number_text in {"", "-", ".", "-."}:
            raise ValueError(f"Invalid numeric value parsed from: {Phrase!r}")
        return number_text

    @classmethod
    def _MergeTensAndUnits(cls, Tokens: list[str]) -> list[str]:
        """Merge "tens [connector] unit" sequences into one number token.

        Lets users say a natural compound number ("treinta y dos", "twenty
        two", "vinte e um") instead of dictating each digit separately. A
        lone digit word with no preceding tens word is left untouched, so
        digit-by-digit dictation (saying "uno" "uno" for 11) still works.
        """
        merged: list[str] = []
        index, total = 0, len(Tokens)
        while index < total:
            token = Tokens[index]
            if token in cls.TensWords:
                lookahead = index + 1
                if lookahead < total and Tokens[lookahead] in cls.ConnectorWords:
                    lookahead += 1
                if lookahead < total and Tokens[lookahead] in cls.UnitWords:
                    merged.append(str(cls.TensWords[token] + cls.UnitWords[Tokens[lookahead]]))
                    index = lookahead + 1
                    continue
            merged.append(token)
            index += 1
        return merged

    @classmethod
    def Tokenize(cls, Phrase: str) -> list[str]:
        """Normalize and split a phrase into parseable tokens."""
        normalized = cls.NormalizeText(Phrase)
        return re.findall(r"-?\d+(?:[.,]\d+)?|[a-z0-9]+", normalized)

    @staticmethod
    def NormalizeText(Text: str) -> str:
        """Remove accents and normalize common decimal punctuation."""
        if not Text:
            return ""
        normalized = (
            unicodedata.normalize("NFKD", Text)
            .encode("ASCII", "ignore")
            .decode()
            .lower()
        )
        return normalized.replace(",", ".")

    @classmethod
    def _TokenToNumericText(cls, Token: str) -> str | None:
        if Token in cls.DigitWords:
            return cls.DigitWords[Token]
        if re.fullmatch(r"-?\d+(?:\.\d+)?", Token):
            return Token
        return None


def _LoadNavWordsFromDictionaries() -> None:
    """Widen the confirm/cancel sets with NavCommands/TraduceTo*.py.

    Los prompts aceptan los tres idiomas a la vez, asi que se juntan los tres
    TraduceTo. Si el diccionario no esta o falla la importacion, quedan los
    conjuntos escritos en la clase: los prompts siguen andando con las palabras
    basicas en vez de romper el arranque.
    """
    try:
        import importlib
        import sys

        from integration.voice_bootstrap import _resolve_dictionary_root

        root = _resolve_dictionary_root()
        if not (root / "NavCommands").is_dir():
            return

        parent = str(root.parent)
        if parent not in sys.path:
            sys.path.insert(0, parent)

        package = root.name
        actions = importlib.import_module(f"{package}.NavCommands.NavActions").NavActions
        send, cancel = actions.get("send"), actions.get("cancel")

        for lang in ("TraduceToEs", "TraduceToEn", "TraduceToPT"):
            module = importlib.import_module(f"{package}.NavCommands.{lang}")
            mapping = getattr(module, lang, {})
            for spoken, target in mapping.items():
                raw = spoken.strip().lower()
                normalized = SpokenNumberParser.NormalizeText(raw).strip()
                if target is send:
                    SpokenNumberParser.ConfirmationWords.add(raw)
                    if normalized != raw:
                        SpokenNumberParser.ConfirmationWords.add(normalized)
                elif target is cancel:
                    SpokenNumberParser.CancellationWords.add(raw)
                    if normalized != raw:
                        SpokenNumberParser.CancellationWords.add(normalized)
    except Exception:
        # Un diccionario roto no puede dejar los prompts sin confirmar.
        pass


_LoadNavWordsFromDictionaries()

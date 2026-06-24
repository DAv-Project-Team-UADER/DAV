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
        "diez": "10",
        "ten": "10",
        "dez": "10",
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
    ConfirmationWords: set[str] = {
        "enter",
        "entrar",
        "enviar",
        "send",
        "ok",
        "aceptar",
        "aceitar",
        "confirmar",
    }
    CancellationWords: set[str] = {"cancelar", "cancel", "cancela", "cancelamento"}

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

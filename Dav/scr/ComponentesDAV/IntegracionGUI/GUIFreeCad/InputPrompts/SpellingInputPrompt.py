#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Build a text letter by letter by voice."""

from __future__ import annotations

from InputPrompts.BaseInputPrompt import BaseInputPrompt
from InputPrompts.PlaneGrammarSwitcher import PlaneGrammarSwitcher
from InputPrompts.PromptResult import PromptResult
from InputPrompts.SpokenNumberParser import SpokenNumberParser

_ENYE = "qenyeq"  # la Ñ se protege antes de que NormalizeText le quite la tilde


def _Prep(Text: str) -> str:
    return SpokenNumberParser.NormalizeText(Text.lower().replace("eñe", _ENYE).replace("ñ", _ENYE))


class SpellingInputPrompt(BaseInputPrompt):
    """Say letter names, digits, ``espacio`` and ``borrar``; confirm with okey."""

    MaxLength = 40

    LetterNames: dict[str, dict[str, str]] = {
        "es": {
            "a": "A", "be": "B", "ce": "C", "de": "D", "e": "E", "efe": "F", "ge": "G",
            "hache": "H", "i": "I", "jota": "J", "ka": "K", "ele": "L", "eme": "M",
            "ene": "N", "eñe": "Ñ", "ñ": "Ñ", "o": "O", "pe": "P", "cu": "Q",
            "erre": "R", "ese": "S", "te": "T", "u": "U", "uve": "V", "equis": "X",
            "zeta": "Z", "ve": "V", "ye": "Y", "ere": "R", "ache": "H",
        },
        "en": {
            "a": "A", "bee": "B", "cee": "C", "dee": "D", "e": "E", "eff": "F", "gee": "G",
            "aitch": "H", "i": "I", "jay": "J", "kay": "K", "el": "L", "em": "M",
            "en": "N", "o": "O", "pee": "P", "cue": "Q", "ar": "R", "ess": "S",
            "tee": "T", "u": "U", "vee": "V", "ex": "X", "why": "Y", "zee": "Z",
            # homofonos que Vosk devuelve en lugar del nombre de la letra
            "see": "C", "sea": "C", "tea": "T", "you": "U", "are": "R", "eye": "I",
            "oh": "O", "pea": "P", "queue": "Q", "zed": "Z",
        },
        "pt": {
            "a": "A", "bê": "B", "cê": "C", "dê": "D", "e": "E", "gê": "G", "agá": "H",
            "i": "I", "jota": "J", "cá": "K", "éle": "L", "ême": "M", "o": "O",
            "pê": "P", "quê": "Q", "érre": "R", "ésse": "S", "tê": "T", "u": "U",
            "vê": "V", "xis": "X", "ípsilon": "Y", "zê": "Z", "fê": "F", "efe": "F", "ene": "N",
            "dáblio": "W", "dábliu": "W", "dâblio": "W", "capa": "K", "guê": "G",
        },
    }
    # letras y simbolos de dos palabras: (primera, segunda) -> caracter
    PairNames: dict[tuple[str, str], str] = {
        ("doble", "uve"): "W", ("doble", "ve"): "W", ("doble", "u"): "W",
        ("i", "griega"): "Y", ("i", "grego"): "Y",
        ("double", "u"): "W", ("duplo", "ve"): "W",
        ("guion", "bajo"): "_",
    }
    PairWords: dict[str, tuple[str, ...]] = {
        "es": ("doble", "uve", "griega", "bajo"), "en": ("double",), "pt": ("duplo", "grego"),
    }
    # simbolos de una palabra, para nombres de archivo o de croquis ("Sketch_1")
    SymbolNames: dict[str, dict[str, str]] = {
        "es": {"guion": "-", "punto": "."},
        "en": {"dash": "-", "dot": ".", "underscore": "_"},
        "pt": {"hífen": "-", "ponto": ".", "sublinhado": "_"},
    }
    # "<letra> de <palabra clave>" ("be de boca", "cu de queso"): la palabra clave
    # decide la letra aunque Vosk confunda el nombre ("u"/"cu", "de"/"ge"...).
    # Solo espanol; todas estan en el vocabulario del modelo small-es (ni "eñe"
    # ni "ñandú" ni "xilófono" lo estan, por eso "ñu" y "xerox").
    AnchorConnector: str = "de"
    AnchorWords: dict[str, dict[str, str]] = {
        "es": {
            "avión": "A", "boca": "B", "casa": "C", "dedo": "D", "elefante": "E",
            "fuego": "F", "gato": "G", "hilo": "H", "isla": "I", "jirafa": "J",
            "kilo": "K", "luna": "L", "mano": "M", "nariz": "N", "ñu": "Ñ",
            "oso": "O", "pato": "P", "queso": "Q", "kiosko": "Q", "kiosco": "Q",
            "quiosco": "Q", "rata": "R", "sol": "S", "taza": "T", "uva": "U",
            "vaca": "V", "whisky": "W", "xerox": "X", "taxi": "X", "yate": "Y",
            "zapato": "Z",
        },
    }
    # como se dice cada letra delante de su palabra clave, para la gramatica
    AnchorLetterSpeech: dict[str, str] = {
        "A": "a", "B": "be", "C": "ce", "D": "de", "E": "e", "F": "efe", "G": "ge",
        "H": "hache", "I": "i", "J": "jota", "K": "ka", "L": "ele", "M": "eme",
        "N": "ene", "Ñ": "ñ", "O": "o", "P": "pe", "Q": "cu", "R": "erre", "S": "ese",
        "T": "te", "U": "u", "V": "uve", "W": "doble uve", "X": "equis", "Y": "i griega",
        "Z": "zeta",
    }
    SpaceWords: dict[str, str] = {"es": "espacio", "en": "space", "pt": "espaço"}
    DeleteWords: dict[str, str] = {"es": "borrar", "en": "delete", "pt": "apagar"}

    SpaceTokens: set[str] = {_Prep(word) for word in SpaceWords.values()}
    DeleteTokens: set[str] = {_Prep(word) for word in DeleteWords.values()}

    _Lookup: dict[str, str] = {
        _Prep(name): letter
        for names in LetterNames.values()
        for name, letter in names.items()
    }
    _SymbolLookup: dict[str, str] = {
        _Prep(name): symbol
        for names in SymbolNames.values()
        for name, symbol in names.items()
    }
    _PairLookup: dict[tuple[str, str], str] = {
        (_Prep(first), _Prep(second)): letter for (first, second), letter in PairNames.items()
    }
    _PairFirst: set[str] = {first for first, _second in _PairLookup}
    _AnchorLookup: dict[str, str] = {
        _Prep(word): letter
        for words in AnchorWords.values()
        for word, letter in words.items()
    }
    _AnchorConnector: str = _Prep(AnchorConnector)

    def __init__(self, Title: str = "DAV", Message: str = "", Parent=None) -> None:
        super().__init__(Title, Message, Parent)
        self._Text = ""
        self._Refresh()

    @classmethod
    def GrammarPhrases(cls, Language: str) -> list[str]:
        """Return letter names, digits, space, delete, confirm and cancel words."""
        language = Language if Language in cls.LetterNames else "es"
        phrases = list(cls.LetterNames[language])
        phrases.extend(cls.PairWords[language])
        phrases.extend(cls.SymbolNames[language])
        phrases.extend(
            f"{cls.AnchorLetterSpeech[letter]} {cls.AnchorConnector} {word}"
            for word, letter in cls.AnchorWords.get(language, {}).items()
        )
        # "un" suena casi igual que la letra "u" y Vosk la cambiaba por el digito 1
        phrases.extend(
            word
            for word, value in SpokenNumberParser.DigitWords.items()
            if len(value) == 1 and word != "un"
        )
        phrases.extend([cls.SpaceWords[language], cls.DeleteWords[language]])
        # confirmar y cancelar, sin arriba/abajo (los dos primeros de la lista)
        phrases.extend(PlaneGrammarSwitcher.PlanePhrases(language)[2:])
        seen: set[str] = set()
        return [word for word in phrases if not (word in seen or seen.add(word))]

    def GetText(self) -> str:
        """Return the text built so far."""
        return self._Text

    def ProcessPartialText(self, Text: str) -> None:
        """Ignore partials: a letter counts only in the final result."""

    def ProcessFinalText(self, Text: str) -> PromptResult:
        """Apply the spoken letters; stop at a confirmation word; cancel aborts."""
        tokens = SpokenNumberParser.Tokenize(_Prep(Text))
        if set(tokens) & SpokenNumberParser.CancellationWords:
            return self.Cancel()

        digits = SpokenNumberParser.DigitWords
        index = 0
        while index < len(tokens):
            token = tokens[index]
            following = tokens[index + 1] if index + 1 < len(tokens) else ""
            anchored = self._MatchAnchor(tokens, index)
            if anchored is not None:
                letter, used = anchored
                self._Append(letter)
                index += used
                continue
            if token in self._PairFirst and (token, following) in self._PairLookup:
                self._Append(self._PairLookup[(token, following)])
                index += 2
                continue
            index += 1
            if token in SpokenNumberParser.ConfirmationWords:
                self._Refresh()
                return self.AcceptValue(self._Text)
            if token in self.SpaceTokens:
                self._Append(" ")
            elif token in self.DeleteTokens:
                self._Text = self._Text[:-1]
            elif token == _ENYE:
                self._Append("Ñ")
            elif token in self._Lookup:
                self._Append(self._Lookup[token])
            elif token in self._SymbolLookup:
                self._Append(self._SymbolLookup[token])
            elif token in digits and len(digits[token]) == 1:
                self._Append(digits[token])
            elif len(token) == 1 and token.isalnum():
                self._Append(token.upper())
        self._Refresh()
        return self.GetResult()

    @classmethod
    def _MatchAnchor(cls, Tokens: list[str], Index: int) -> tuple[str, int] | None:
        """Match "<letra> de <palabra clave>" starting at ``Index``.

        La palabra clave manda: si Vosk oyo mal el nombre de la letra o lo
        perdio, igual se escribe la letra de la palabra clave.

        Returns:
            La letra y la cantidad de palabras que consumio, o None.
        """
        connector, lookup = cls._AnchorConnector, cls._AnchorLookup
        at = lambda offset: Tokens[Index + offset] if Index + offset < len(Tokens) else ""  # noqa: E731
        # nombre de dos palabras: "doble uve de whisky"
        if (at(0), at(1)) in cls._PairLookup and at(2) == connector and at(3) in lookup:
            return lookup[at(3)], 4
        # una palabra de nombre: "be de boca" (incluye "de de dedo")
        if at(1) == connector and at(2) in lookup:
            return lookup[at(2)], 3
        # el nombre se perdio: "de boca"
        if at(0) == connector and at(1) in lookup:
            return lookup[at(1)], 2
        return None

    def _Append(self, Char: str) -> None:
        if len(self._Text) < self.MaxLength:
            self._Text += Char

    def _Refresh(self) -> None:
        self.SetHeardText(self._Text + "_")
        self.SetStatus(self._StatusText())

    def _StatusText(self) -> str:
        return f"{len(self._Text)}/{self.MaxLength} — letras, espacio, borrar, okey, cancelar"

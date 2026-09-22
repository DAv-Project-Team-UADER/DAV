#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Yes/no question answered by voice."""

from __future__ import annotations

from InputPrompts.BaseInputPrompt import BaseInputPrompt
from InputPrompts.PromptResult import PromptResult
from InputPrompts.SpokenNumberParser import SpokenNumberParser

_YES = {
    "si", "okey", "okay", "ok", "dale", "aceptar", "confirmar", "listo", "vale",
    "yes", "yep", "accept", "confirm", "sim", "aceitar", "pronto",
}
_NO = {"no", "negativo", "nope", "negative", "nao"}
_CANCEL = {
    "cancelar", "cancela", "abortar", "anular", "descartar",
    "cancel", "abort", "discard", "cancelamento",
}
_PHRASES = {
    "es": ["si", "sí", "okey", "ok", "dale", "aceptar", "confirmar", "listo", "vale",
           "no", "negativo", "cancelar", "cancela", "abortar", "anular", "descartar"],
    "en": ["yes", "yep", "okey", "ok", "accept", "confirm", "no", "nope", "negative",
           "cancel", "abort", "discard"],
    "pt": ["sim", "okey", "ok", "aceitar", "confirmar", "pronto", "não", "nao", "negativo",
           "cancelar", "cancelamento", "abortar", "anular"],
}


class YesNoInputPrompt(BaseInputPrompt):
    """Ask a question; accepts ``True`` (yes) or ``False`` (no). Cancel aborts."""

    def __init__(self, Title: str = "DAV", Message: str = "", Parent=None) -> None:
        super().__init__(Title, Message, Parent)
        # el botón Aceptar responde «sí» en vez de devolver el texto escuchado
        self._OkButton.clicked.disconnect()
        self._OkButton.clicked.connect(lambda: self.AcceptValue(True))

    def GrammarPhrases(self, Language: str) -> list[str]:
        """Return the phrases Vosk should listen for."""
        return list(_PHRASES.get(Language, _PHRASES["es"]))

    def ProcessFinalText(self, Text: str) -> PromptResult:
        """Cancel first, then no, then yes."""
        self.SetHeardText(Text)
        tokens = set(SpokenNumberParser.Tokenize(Text))
        if tokens & _CANCEL:
            return self.Cancel()
        if tokens & _NO:
            return self.AcceptValue(False)
        if tokens & _YES:
            return self.AcceptValue(True)
        self.SetStatus("No te entendí")
        return self.GetResult()

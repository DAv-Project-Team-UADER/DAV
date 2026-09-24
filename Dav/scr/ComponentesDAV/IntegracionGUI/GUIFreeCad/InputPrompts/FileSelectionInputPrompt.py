#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Voice folder browser: next/previous, open a folder, go up, confirm."""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from InputPrompts.BaseInputPrompt import BaseInputPrompt
from InputPrompts.PlaneGrammarSwitcher import PlaneGrammarSwitcher
from InputPrompts.PromptResult import PromptResult
from InputPrompts.SpokenNumberParser import SpokenNumberParser

_WORDS: dict[str, dict[str, tuple[str, ...]]] = {
    "es": {
        "next": ("siguiente", "avanzar", "abajo", "próximo", "otro"),
        "previous": ("anterior", "atrás", "retroceder", "arriba", "previo"),
        "parent": ("subir", "padre"),
        "enter": ("abrir", "adentro"),
        "choose": ("elegir", "seleccionar"),
    },
    "en": {
        "next": ("next", "forward", "down", "advance"),
        "previous": ("previous", "back", "up"),
        "parent": ("parent", "out"),
        "enter": ("open", "inside"),
        "choose": ("choose", "select"),
    },
    "pt": {
        "next": ("seguinte", "próximo", "abaixo"),
        "previous": ("anterior", "voltar", "cima"),
        "parent": ("subir", "pai"),
        "enter": ("abrir", "dentro"),
        "choose": ("escolher", "selecionar"),
    },
}


def _All(Kind: str) -> set[str]:
    return {
        SpokenNumberParser.NormalizeText(word)
        for table in _WORDS.values()
        for word in table[Kind]
    }


class FileSelectionInputPrompt(BaseInputPrompt):
    """Browse folders by voice; accepts the chosen path as text."""

    def __init__(
        self,
        StartDir: Path,
        Extensions: Iterable[str] | None = None,
        FoldersOnly: bool = False,
        Title: str = "DAV",
        Message: str = "",
        Parent=None,
    ) -> None:
        super().__init__(Title, Message, Parent)
        self._Dir = Path(StartDir)
        self._Extensions = {ext.lower().lstrip(".") for ext in (Extensions or ())}
        self._FoldersOnly = FoldersOnly
        self._Entries: list[Path] = []
        self._CurrentIndex = 0
        self._Notice = ""
        self._Load()
        self._Refresh()

    def GrammarPhrases(self, Language: str) -> list[str]:
        """Return navigation words plus the confirm and cancel phrases."""
        phrases = [word for words in _WORDS.get(Language, _WORDS["es"]).values() for word in words]
        phrases.extend(word for word in PlaneGrammarSwitcher.PlanePhrases(Language) if word not in phrases)
        return phrases

    def GetCurrentDir(self) -> Path:
        """Return the folder being browsed."""
        return self._Dir

    def GetSelectedPath(self) -> Path:
        """Return the highlighted entry (the current folder when none)."""
        if self._FoldersOnly or not self._Entries:
            return self._Dir
        return self._Entries[self._CurrentIndex]

    def ProcessFinalText(self, Text: str) -> PromptResult:
        """Cancel, go up, enter, move or confirm."""
        self.SetHeardText(Text)
        tokens = set(SpokenNumberParser.Tokenize(Text))
        self._Notice = ""

        if tokens & SpokenNumberParser.CancellationWords:
            return self.Cancel()
        if tokens & _All("parent"):
            self._GoUp()
        elif tokens & _All("enter"):
            if self._Entries and self._Entries[self._CurrentIndex].is_dir():
                self._EnterSelected()
            elif self._Entries:
                return self._Confirm()
        elif tokens & _All("next"):
            self._Step(1)
        elif tokens & _All("previous"):
            self._Step(-1)
        elif tokens & _All("choose") or self._HasConfirmation(list(tokens)):
            return self._Confirm()
        self._Refresh()
        return self.GetResult()

    def _Load(self) -> None:
        try:
            entries = [
                entry for entry in self._Dir.iterdir()
                if not entry.name.startswith(".") and self._Matches(entry)
            ]
        except OSError as error:
            self._Notice = str(error)
            entries = []
        entries.sort(key=lambda entry: (not entry.is_dir(), entry.name.casefold()))
        self._Entries = entries
        self._CurrentIndex = 0

    def _Matches(self, Entry: Path) -> bool:
        try:
            if Entry.is_dir():
                return True
            return not self._FoldersOnly and (
                not self._Extensions or Entry.suffix.lower().lstrip(".") in self._Extensions
            )
        except OSError:
            return False

    def _Step(self, Direction: int) -> None:
        if self._Entries:
            self._CurrentIndex = (self._CurrentIndex + Direction) % len(self._Entries)

    def _GoUp(self) -> None:
        parent = self._Dir.parent
        if parent == self._Dir:
            self._Notice = "Ya estás en la carpeta raíz."
            return
        self._Dir = parent
        self._Load()

    def _EnterSelected(self) -> None:
        self._Dir = self._Entries[self._CurrentIndex]
        self._Load()

    def _Confirm(self) -> PromptResult:
        if self._FoldersOnly:
            return self.AcceptValue(str(self._Dir))
        if not self._Entries:
            self._Notice = "No hay nada para elegir acá."
            self._Refresh()
            return self.GetResult()
        selected = self._Entries[self._CurrentIndex]
        if selected.is_dir():
            self._EnterSelected()
            self._Refresh()
            return self.GetResult()
        return self.AcceptValue(str(selected))

    def _Refresh(self) -> None:
        intro = self._Message.splitlines()[0] if self._Message else ""
        self.SetMessage(f"{intro}\n{self._Dir}".strip())
        if self._Entries:
            entry = self._Entries[self._CurrentIndex]
            self.SetHeardText(f"{entry.name}{'/' if entry.is_dir() else ''}")
            position = f"({self._CurrentIndex + 1}/{len(self._Entries)}) "
        else:
            self.SetHeardText("(vacío)")
            position = ""
        self.SetStatus(
            self._Notice or f"{position}siguiente/anterior, abrir, subir, okey, cancelar"
        )

#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Non-modal player that walks a guided example one frame at a time."""

from __future__ import annotations

import html

try:
    from PySide6.QtCore import Qt
    from PySide6.QtWidgets import QLabel
except ImportError:
    from PySide2.QtCore import Qt  # type: ignore[assignment]
    from PySide2.QtWidgets import QLabel  # type: ignore[assignment]

from InputPrompts.BaseInputPrompt import BaseInputPrompt
from InputPrompts.ExampleStep import NAVIGATION_WORDS, WORD_SYNONYMS, ExampleStep
from InputPrompts.PlaneGrammarSwitcher import PlaneGrammarSwitcher
from InputPrompts.PromptResult import PromptResult
from InputPrompts.SpokenNumberParser import SpokenNumberParser

_LABELS = {
    "es": {"skip": "Saltar cuadro", "close": "Cerrar", "done": "Ejemplo terminado. Decí enviar para cerrar."},
    "en": {"skip": "Skip frame", "close": "Close", "done": "Example finished. Say send to close."},
    "pt": {"skip": "Pular quadro", "close": "Fechar", "done": "Exemplo concluído. Diga enviar para fechar."},
}


def _PlayerWindowFlags():
    """Return the flags of a real window: the player can be minimised and maximised.

    A plain ``QDialog`` has no minimise or maximise button, so while an example was
    running its window could only be moved or closed.
    """
    flags = Qt.WindowType if hasattr(Qt, "WindowType") else Qt
    return (
        flags.Window
        | flags.WindowMinimizeButtonHint
        | flags.WindowMaximizeButtonHint
        | flags.WindowCloseButtonHint
    )


def _Canonical(Word: str) -> str:
    return WORD_SYNONYMS.get(Word, Word)


def _AllWords(Kind: str) -> set[str]:
    words = (word for table in NAVIGATION_WORDS.values() for word in table[Kind])
    return {SpokenNumberParser.NormalizeText(word) for word in words}


class GuidedExampleInputPrompt(BaseInputPrompt):
    """Show one frame at a time; run its action once all its words were said."""

    def __init__(self, Title: str, Steps: list[ExampleStep], Parent=None) -> None:
        super().__init__(Title, "", Parent)
        self._Steps = list(Steps)
        self._Viewing = 0
        self._Pending = 0
        self._Matched = 0
        self._PendingWords: list[str] = []
        self._Labels = _LABELS.get(self._Language, _LABELS["es"])

        self.setModal(False)
        self.setWindowFlags(_PlayerWindowFlags())
        self.setSizeGripEnabled(True)
        self._ChipsLabel = QLabel(self)
        self._ChipsLabel.setWordWrap(True)
        self._ChipsLabel.setTextFormat(Qt.TextFormat.RichText)
        self.layout().insertWidget(1, self._ChipsLabel)
        # al maximizar, el sobrante va aquí: el texto queda arriba y los botones abajo
        self.layout().insertStretch(4)

        # Aceptar pasa a ser «Saltar cuadro» y Cancelar pasa a ser «Cerrar»
        self._OkButton.clicked.disconnect()
        self._OkButton.clicked.connect(self.SkipStep)
        self._OkButton.setText(self._Labels["skip"])
        self._CancelButton.setText(self._Labels["close"])

        self._LoadPending()
        self._Render()

    # ------------------------------------------------------------------ voz

    def GrammarPhrases(self, Language: str) -> list[str]:
        """Return navigation, cancel and the words of the current frame.

        Each word goes in with and without its accents. Vosk can only return words
        that exist in the model's lexicon, and the lexicon is accented ("geometría",
        not "geometria"): sending both spellings leaves the one the model knows and
        drops the other, so the frame can be dictated whichever way it is written.
        """
        table = NAVIGATION_WORDS.get(Language, NAVIGATION_WORDS["es"])
        phrases = [*table["previous"], *table["next"], *table["select"], *table["skip"]]
        cancel = SpokenNumberParser.CancellationWords
        phrases.extend(
            word
            for word in PlaneGrammarSwitcher.PlanePhrases(Language)
            if SpokenNumberParser.NormalizeText(word) in cancel
        )
        if self._Viewing < len(self._Steps):
            for phrase in self._Steps[self._Viewing].GetSay(Language):
                for word in phrase.split():
                    for spelling in (word, SpokenNumberParser.NormalizeText(word)):
                        if spelling and spelling not in phrases:
                            phrases.append(spelling)
        return phrases

    def ProcessFinalText(self, Text: str) -> PromptResult:
        """Match the frame's words first, then skip, review, close or cancel."""
        self.SetHeardText(Text)
        tokens = SpokenNumberParser.Tokenize(Text)
        tokens_set = set(tokens)

        if self._Pending < len(self._Steps) and self._Viewing == self._Pending:
            if self._Consume(Text):
                return self.GetResult()

        if tokens_set & SpokenNumberParser.CancellationWords:
            return self.Cancel()
        if self._Pending < len(self._Steps) and tokens_set & _AllWords("skip"):
            self.SkipStep()
            return self.GetResult()
        if tokens_set & _AllWords("previous"):
            self._View(self._Viewing - 1)
            return self.GetResult()
        if tokens_set & _AllWords("next"):
            self._View(self._Viewing + 1)
            return self.GetResult()
        if self._Pending >= len(self._Steps) and (
            tokens_set & _AllWords("select") or self._HasConfirmation(tokens)
        ):
            return self.AcceptValue(True)
        return self.GetResult()

    def _Consume(self, Text: str) -> bool:
        """Advance over the pending words heard in ``Text``; True if any matched."""
        words = self._PendingWords
        before = self._Matched
        for token in SpokenNumberParser.Tokenize(Text):
            if self._Matched < len(words) and _Canonical(token) == words[self._Matched]:
                self._Matched += 1
        if self._Matched == before:
            return False
        if self._Matched >= len(words):
            self._RunPending()
        else:
            self._Render()
        return True

    # ------------------------------------------------------------ acciones

    def SkipStep(self) -> None:
        """Run the pending frame without saying its words."""
        if self._Pending < len(self._Steps):
            self._RunPending()

    def _RunPending(self) -> None:
        step = self._Steps[self._Pending]
        try:
            step.Action()
        except Exception as error:
            self._Matched = 0
            self._Render()
            self.Fail(str(error))
            return
        self._Pending += 1
        self._Viewing = self._Pending
        self._LoadPending()
        self._Render()

    def _LoadPending(self) -> None:
        """Compute the words of the pending frame (they may depend on the document)."""
        self._Matched = 0
        self._PendingWords = []
        if self._Pending < len(self._Steps):
            say = self._Steps[self._Pending].GetSay(self._Language)
            self._PendingWords = [
                _Canonical(token)
                for phrase in say
                for token in SpokenNumberParser.Tokenize(phrase)
            ]

    def _View(self, Index: int) -> None:
        """Look at another frame; frames after the pending one are off limits."""
        self._Viewing = max(0, min(Index, self._Pending))
        self._Render()

    # ---------------------------------------------------------- ventana

    def Show(self) -> None:
        """Show the window at the bottom right of the editor, without blocking it."""
        self.setModal(False)
        self.show()
        parent = self.parentWidget()
        if parent is not None:
            frame = parent.frameGeometry()
            self.move(
                frame.right() - self.width() - 24,
                frame.bottom() - self.height() - 48,
            )
        self.raise_()
        self.activateWindow()

    def done(self, Code) -> None:
        """Restore the CAD grammar when the window closes."""
        PlaneGrammarSwitcher.RestoreCadGrammar()
        super().done(Code)

    # ---------------------------------------------------------- dibujo

    def _Chips(self, Words: list[str], IsDone: bool) -> list[str]:
        """Group consecutive repeats («abajo ×3») and mark what was already said."""
        groups: list[list] = []
        for word in Words:
            if groups and groups[-1][0] == word:
                groups[-1][1] += 1
            else:
                groups.append([word, 1])
        chips = []
        spent = len(Words) if IsDone else self._Matched
        position = 0
        for word, count in groups:
            said = max(0, min(count, spent - position))
            position += count
            label = html.escape(word)
            if count > 1:
                label += f" ×{count}" if said in (0, count) else f" {said}/{count}"
            done = said == count
            style = (
                "background:#2e7d32;color:#fff;"
                if done
                else "background:#888;color:#fff;" if said else "background:#ccc;color:#000;"
            )
            chips.append(f'<span style="{style} padding:2px 6px;">{label}</span>')
        return chips

    def _Render(self) -> None:
        if self._Viewing >= len(self._Steps):
            self.SetMessage(self._Labels["done"])
            self._ChipsLabel.setText("")
            self.SetStatus(f"({len(self._Steps)}/{len(self._Steps)})")
            self._OkButton.setEnabled(False)
        else:
            step = self._Steps[self._Viewing]
            is_done = self._Viewing < self._Pending
            words = (
                [
                    _Canonical(token)
                    for phrase in step.GetSay(self._Language)
                    for token in SpokenNumberParser.Tokenize(phrase)
                ]
                if is_done
                else self._PendingWords
            )
            self.SetMessage(step.GetText(self._Language))
            self._ChipsLabel.setText(" ".join(self._Chips(words, is_done)))
            self.SetStatus(f"({self._Viewing + 1}/{len(self._Steps)})")
            self._OkButton.setEnabled(self._Pending < len(self._Steps))
        self._ApplyGrammar()

    def _ApplyGrammar(self) -> None:
        PlaneGrammarSwitcher.ActivateGrammar(self.GrammarPhrases(self._Language))

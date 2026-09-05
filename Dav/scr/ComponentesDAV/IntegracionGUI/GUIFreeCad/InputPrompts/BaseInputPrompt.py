#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Reusable base dialog for DAV voice-driven input prompts."""

from __future__ import annotations

from typing import Any

try:
    from PySide6.QtCore import Qt, Signal
    from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout
except ImportError:
    from PySide2.QtCore import Qt, Signal  # type: ignore[assignment]
    from PySide2.QtWidgets import QDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout  # type: ignore[assignment]

from InputPrompts.PromptResult import PromptResult
from InputPrompts.InputPromptI18n import ResolveLanguage, T


def _AlignCenter():
    if hasattr(Qt, "AlignmentFlag"):
        return Qt.AlignmentFlag.AlignCenter
    return Qt.AlignCenter


class BaseInputPrompt(QDialog):
    """Base Qt dialog used by concrete input prompt implementations."""

    ResultReady = Signal(object)

    def __init__(
        self,
        Title: str = "DAV Input",
        Message: str = "Say a value",
        Parent=None,
    ) -> None:
        super().__init__(Parent)
        self._Language = ResolveLanguage()
        self._Title = Title
        self._Message = Message
        self._Result = PromptResult.Pending()
        self._AccumulatedText = ""
        self._BuildUi()
        self.SetTitle(Title)
        self.SetMessage(Message)
        self.SetStatus(T(self._Language, "listening"))

    def _BuildUi(self) -> None:
        self.setModal(True)
        self.setMinimumWidth(420)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        self._MessageLabel = QLabel(self)
        self._MessageLabel.setWordWrap(True)
        self._MessageLabel.setAlignment(_AlignCenter())
        layout.addWidget(self._MessageLabel)

        self._StatusLabel = QLabel(self)
        self._StatusLabel.setAlignment(_AlignCenter())
        self._StatusLabel.setStyleSheet("color: #555555; font-size: 9pt;")
        layout.addWidget(self._StatusLabel)

        self._HeardLabel = QLabel(self)
        self._HeardLabel.setWordWrap(True)
        self._HeardLabel.setAlignment(_AlignCenter())
        self._HeardLabel.setStyleSheet(
            "background: #f3f3f3; border: 1px solid #d8d8d8; padding: 8px;"
        )
        layout.addWidget(self._HeardLabel)

        button_row = QHBoxLayout()
        button_row.addStretch()
        self._OkButton = QPushButton(T(self._Language, "ok"), self)
        self._CancelButton = QPushButton(T(self._Language, "cancel"), self)
        self._OkButton.setAutoDefault(False)
        self._OkButton.setDefault(False)
        self._CancelButton.setAutoDefault(False)
        self._CancelButton.setDefault(False)
        self._OkButton.clicked.connect(lambda: self.AcceptValue(self.GetCurrentText()))
        self._CancelButton.clicked.connect(self.Cancel)
        button_row.addWidget(self._OkButton)
        button_row.addWidget(self._CancelButton)
        button_row.addStretch()
        layout.addLayout(button_row)

        self.SetHeardText("")

    def SetTitle(self, Title: str) -> None:
        """Update the dialog title."""
        self._Title = Title
        self.setWindowTitle(Title)

    def SetMessage(self, Message: str) -> None:
        """Update the main prompt message."""
        self._Message = Message
        self._MessageLabel.setText(Message)

    def SetStatus(self, Status: str) -> None:
        """Update the listening/status label."""
        self._StatusLabel.setText(Status)

    def SetHeardText(self, Text: str) -> None:
        """Update the recognized text preview."""
        display = Text.strip() if Text else ""
        self._HeardLabel.setText(display or "...")

    def GetCurrentText(self) -> str:
        """Return the current recognized text shown by the prompt."""
        text = self._HeardLabel.text()
        return "" if text == "..." else text

    def GetResult(self) -> PromptResult:
        """Return the current prompt result."""
        return self._Result

    def ProcessPartialText(self, Text: str) -> None:
        """Process partial recognized text."""
        self.SetHeardText(Text)
        self.SetStatus(T(self._Language, "listening"))

    def ProcessFinalText(self, Text: str) -> PromptResult:
        """Process final recognized text.

        Concrete prompts should override this method when they need parsing or
        validation before accepting the value.
        """
        self.SetHeardText(Text)
        return self.GetResult()

    def RequiresNumericGrammar(self) -> bool:
        """Return True when this prompt needs the Vosk numeric-word grammar.

        Overridden by prompts (see NumericInputPrompt) that collect spoken
        digits, so callers can switch grammar polymorphically instead of
        checking concrete prompt types.
        """
        return False

    @staticmethod
    def _HasConfirmation(Tokens: list[str]) -> bool:
        from InputPrompts.SpokenNumberParser import SpokenNumberParser

        return any(token in SpokenNumberParser.ConfirmationWords for token in Tokens)

    @staticmethod
    def _HasCancellation(Tokens: list[str]) -> bool:
        from InputPrompts.SpokenNumberParser import SpokenNumberParser

        return any(token in SpokenNumberParser.CancellationWords for token in Tokens)

    def AcceptValue(self, Value: Any | None = None) -> PromptResult:
        """Accept the prompt with a value and close the dialog."""
        if isinstance(Value, str) and not Value.strip():
            return self.Fail(T(self._Language, "value_not_empty"))
        self._Result = PromptResult.Ok(Value)
        self.SetStatus(T(self._Language, "accepted"))
        self.ResultReady.emit(self._Result)
        self.accept()
        return self._Result

    def Fail(self, Error: str) -> PromptResult:
        """Store a failed result and keep the dialog open."""
        self._Result = PromptResult.Fail(Error)
        self.SetStatus(Error)
        self.ResultReady.emit(self._Result)
        return self._Result

    def Cancel(self) -> PromptResult:
        """Cancel the prompt and close the dialog."""
        self._Result = PromptResult.Cancel()
        self.SetStatus(T(self._Language, "cancelled"))
        self.ResultReady.emit(self._Result)
        self.reject()
        return self._Result

    def Show(self) -> None:
        """Show the prompt without blocking the caller."""
        self.show()
        self.raise_()
        self.activateWindow()

    def RequestValue(self) -> PromptResult:
        """Show the prompt modally and return its result."""
        self._ExecDialog()
        return self.GetResult()

    def reject(self) -> None:
        """Treat closing the dialog as cancellation."""
        if self._Result.Success:
            super().reject()
            return
        self._Result = PromptResult.Cancel()
        super().reject()

    def _ExecDialog(self) -> int:
        if hasattr(self, "exec"):
            return self.exec()
        return self.exec_()

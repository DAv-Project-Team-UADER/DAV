"""Custom dialogs for large-model availability and download prompt."""

from __future__ import annotations

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QDialog, QHBoxLayout, QLabel, QPushButton, QVBoxLayout

from core.i18n import tr


class UnavailableModelDialog(QDialog):
    """Information dialog when large model is missing and there is no internet."""

    def __init__(self, lang: str, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(tr("preferences_title", lang))
        self.setModal(True)
        self.setMinimumWidth(380)

        layout = QVBoxLayout(self)
        msg = QLabel(tr("large_model_unavailable", lang), self)
        msg.setWordWrap(True)
        msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(msg)

        btn = QPushButton("OK", self)
        btn.clicked.connect(self.accept)
        layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)


class UpdateModelDialog(QDialog):
    """Ask user to download large model. 'No' does NOT close the dialog."""

    confirmed = Signal()
    rejected_voice = Signal()

    def __init__(self, lang: str, parent=None) -> None:
        super().__init__(parent)
        self._lang = lang
        self.setWindowTitle(tr("preferences_title", lang))
        self.setModal(True)
        self.setMinimumWidth(400)

        layout = QVBoxLayout(self)
        self._msg = QLabel(tr("update_large_model", lang), self)
        self._msg.setWordWrap(True)
        self._msg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._msg)

        self._voice_hint = QLabel(tr("model_prompt_voice", lang), self)
        self._voice_hint.setWordWrap(True)
        self._voice_hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._voice_hint.setStyleSheet("color: #555555; font-size: 9pt;")
        layout.addWidget(self._voice_hint)

        btn_row = QHBoxLayout()
        self._yes_btn = QPushButton(tr("btn_yes", lang), self)
        self._no_btn = QPushButton(tr("btn_no", lang), self)
        self._yes_btn.clicked.connect(self._on_yes)
        self._no_btn.clicked.connect(self._on_no)
        btn_row.addStretch()
        btn_row.addWidget(self._yes_btn)
        btn_row.addWidget(self._no_btn)
        btn_row.addStretch()
        layout.addLayout(btn_row)

    def _on_yes(self) -> None:
        self.confirmed.emit()
        self.accept()

    def _on_no(self) -> None:
        self.rejected_voice.emit()
        self.reject()

    def trigger_yes(self) -> None:
        self._on_yes()

    def trigger_no(self) -> None:
        self._on_no()

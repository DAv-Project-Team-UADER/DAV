"""Download progress dialog with loading animation."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QMovie
from PySide6.QtWidgets import QDialog, QLabel, QProgressBar, QVBoxLayout

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets"
LOADING_GIF = ASSETS_DIR / "loading.gif"


class DownloadDialog(QDialog):
    def __init__(self, title: str, parent=None) -> None:
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setMinimumWidth(360)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowCloseButtonHint)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        self._gif_label = QLabel(self)
        self._gif_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        if LOADING_GIF.exists():
            movie = QMovie(str(LOADING_GIF))
            self._gif_label.setMovie(movie)
            movie.start()
        else:
            self._dots = 0
            self._gif_label.setText("⏳")
            self._timer = QTimer(self)
            self._timer.timeout.connect(self._animate_dots)
            self._timer.start(400)
        layout.addWidget(self._gif_label)

        self._status = QLabel(title, self)
        self._status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._status)

        self._bar = QProgressBar(self)
        self._bar.setRange(0, 100)
        self._bar.setValue(0)
        layout.addWidget(self._bar)

    def _animate_dots(self) -> None:
        self._dots = (self._dots + 1) % 4
        self._gif_label.setText("⏳" + "." * self._dots)

    def set_message(self, text: str) -> None:
        self._status.setText(text)

    def set_progress(self, current: int, total: int) -> None:
        if total > 0:
            self._bar.setValue(int(current * 100 / total))

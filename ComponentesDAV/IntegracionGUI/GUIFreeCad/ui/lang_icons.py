"""Flag icons for language selectors (Windows/Qt often cannot render flag emojis)."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QLabel

FLAGS_DIR = Path(__file__).resolve().parent.parent / "assets" / "flags"
LANG_FLAG_SIZE = QSize(18, 13)


def lang_icon(language_code: str) -> QIcon:
    path = FLAGS_DIR / f"{language_code}.svg"
    if path.is_file():
        return QIcon(str(path))
    return QIcon()


def apply_lang_flag(label: QLabel, language_code: str) -> None:
    icon = lang_icon(language_code)
    if icon.isNull():
        label.clear()
        return
    label.setPixmap(icon.pixmap(LANG_FLAG_SIZE))
    label.setFixedSize(LANG_FLAG_SIZE)

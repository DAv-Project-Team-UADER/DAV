"""Apply light/dark FreeCAD-like themes."""

from __future__ import annotations

from pathlib import Path

from PySide6.QtWidgets import QApplication

THEMES_DIR = Path(__file__).resolve().parent.parent / "assets" / "themes"


def apply_theme(app: QApplication, theme: str) -> None:
    qss_file = THEMES_DIR / ("dark.qss" if theme == "dark" else "light.qss")
    if qss_file.exists():
        app.setStyleSheet(qss_file.read_text(encoding="utf-8"))
    else:
        app.setStyleSheet("")

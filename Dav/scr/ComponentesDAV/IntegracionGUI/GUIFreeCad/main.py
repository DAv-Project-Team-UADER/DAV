#!/usr/bin/env python3
"""GUIFreeCad — DAV Project voice UI with FreeCAD-style preferences."""

import sys
from pathlib import Path

# Ensure project root is on sys.path
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from PySide6.QtWidgets import QApplication

from core.model_manager import verify_small_models
from core.settings import settings
from ui.main_window import MainWindow
from ui.theme import apply_theme


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("GUIFreeCad")

    apply_theme(app, settings.theme)

    # 1) Verify bundled small models at startup
    verify_small_models()

    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())

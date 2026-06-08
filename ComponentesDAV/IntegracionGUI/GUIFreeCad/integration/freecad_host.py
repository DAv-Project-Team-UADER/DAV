"""Detect FreeCAD runtime and resolve paths for the DAV voice GUI."""

from __future__ import annotations

import os
import sys
from pathlib import Path

GUI_ROOT = Path(__file__).resolve().parent.parent


def in_freecad() -> bool:
    return "FreeCAD" in sys.modules or "FreeCADGui" in sys.modules


def ensure_gui_on_path() -> Path:
    root = str(GUI_ROOT)
    if root not in sys.path:
        sys.path.insert(0, root)
    return GUI_ROOT


def gui_root_from_env() -> Path | None:
    raw = os.environ.get("DAV_GUI_FREECAD_ROOT", "").strip()
    if not raw:
        return None
    path = Path(raw)
    return path if path.is_dir() else None


def resolve_gui_root() -> Path:
    """Return GUIFreeCad root (env override, then this package)."""
    return gui_root_from_env() or GUI_ROOT


def get_freecad_main_window():
    import FreeCADGui

    return FreeCADGui.getMainWindow()


def get_qt_application():
    from PySide6.QtWidgets import QApplication

    app = QApplication.instance()
    if app is None:
        raise RuntimeError("No Qt application instance (expected when running inside FreeCAD).")
    return app

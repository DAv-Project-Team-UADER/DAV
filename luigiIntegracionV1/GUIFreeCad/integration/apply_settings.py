"""Load settings.json and apply theme (and related UI state)."""

from __future__ import annotations

from core.settings import settings
from ui.theme import apply_theme


def apply_saved_settings(app=None) -> None:
    """Re-read config/settings.json and apply theme to the running Qt app."""
    settings.load()
    if app is None:
        try:
            from PySide6.QtWidgets import QApplication
        except ImportError:
            from PySide2.QtWidgets import QApplication  # type: ignore[no-redef]

        app = QApplication.instance()
    if app is not None:
        apply_theme(app, settings.theme)

    try:
        import FreeCAD  # noqa: F401

        from integration.freecad_voice_setup import install_freecad_integration

        install_freecad_integration()
    except ImportError:
        pass

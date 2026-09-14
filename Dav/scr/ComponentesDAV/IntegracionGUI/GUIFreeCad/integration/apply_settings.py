"""Load settings.json and apply theme (and related UI state)."""

from __future__ import annotations

from core.settings import settings
from ui.theme import apply_theme


def apply_report_palette(theme: str) -> None:
    """Set the report view text color via FreeCAD's parameter system.

    ``ReportOutput::OnChange`` observes ``OutputWindow/colorText`` and calls
    ``reportHl->setTextColor()`` when it changes — the only reliable way to
    update the highlighter from outside C++.
    """
    try:
        import FreeCAD as App

        hGrp = App.ParamGet("User parameter:BaseApp/Preferences/OutputWindow")
        # colorText is packed RGB: (R << 24) | (G << 16) | (B << 8)
        white = (0xff << 24) | (0xff << 16) | (0xff << 8)  # 0xFFFFFF00
        black = 0x00000000
        hGrp.SetUnsigned("colorText", white if theme == "dark" else black)
    except Exception:
        pass


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
        from integration.dav_dock_panel import get_source
        src = get_source()
        if src is not None and src._panel is not None:
            src._panel.SetTheme(settings.theme)
            src._panel.SetLanguage(settings.language)
    except Exception:
        pass

    apply_report_palette(settings.theme)

    try:
        import FreeCAD  # noqa: F401

        from integration.freecad_voice_setup import install_freecad_integration

        install_freecad_integration()
    except ImportError:
        pass

    try:
        import FreeCAD  # noqa: F401

        from integration.freecad_voice_setup import install_freecad_integration

        install_freecad_integration()
    except ImportError:
        pass

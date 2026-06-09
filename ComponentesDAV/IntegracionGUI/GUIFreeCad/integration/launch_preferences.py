"""Open DAV preferences inside FreeCAD (or standalone for tests)."""

from __future__ import annotations

from integration.freecad_host import (
    ensure_gui_on_path,
    get_freecad_main_window,
    get_qt_application,
    in_freecad,
)
from core.settings import settings
from ui.preferences_dialog import PreferencesDialog
from ui.theme import apply_theme


def open_preferences(parent=None) -> None:
    ensure_gui_on_path()

    if parent is None and in_freecad():
        parent = get_freecad_main_window()

    dlg = PreferencesDialog(parent)

    def on_changed() -> None:
        apply_theme(get_qt_application(), settings.theme)

    dlg.settings_changed.connect(on_changed)
    dlg.exec()

    if in_freecad():
        from integration.freecad_ui_setup import show_report_view_instead_of_python
        from speech.dav_voice_service import DavVoiceService

        show_report_view_instead_of_python(persist_prefs=False)
        DavVoiceService.get().resume_cad_voice()
        _hint_after_preferences()


def _hint_after_preferences() -> None:
    try:
        import FreeCAD as App
        from integration.voice_bootstrap import is_voice_running

        if is_voice_running():
            App.Console.PrintMessage(
                "[DAV] Preferencias cerradas. Voz CAD reanudada "
                "(«archivo enviar», «preferencias enviar», etc.).\n"
            )
    except ImportError:
        pass

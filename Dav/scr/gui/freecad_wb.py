"""Logica del workbench DAV (importado como modulo Python normal)."""

from __future__ import annotations

import importlib
import os
import sys
import traceback

_DAV_TOOLBAR_COMMANDS = (
    "DAV_OpenPreferences",
    "DAV_StartVoice",
    "DAV_StopVoice",
)


def setup_mod_path() -> str:
    import FreeCAD as App

    mod_dir = ""
    for path in getattr(App, "__ModDirs__", ()) or ():
        norm = os.path.normpath(path)
        if os.path.basename(norm).upper() == "DAV":
            mod_dir = norm
            break
    if not mod_dir:
        env = os.environ.get("DAV_MOD_ROOT", "").strip()
        if env and os.path.isdir(env):
            mod_dir = os.path.normpath(env)
    if not mod_dir:
        user = os.path.join(App.getUserAppDataDir(), "Mod", "DAV")
        if os.path.isdir(user):
            mod_dir = user
    if mod_dir and mod_dir not in sys.path:
        sys.path.insert(0, mod_dir)
    return mod_dir


def apply_dav_toolbar(workbench) -> None:
    """Menu y barra DAV (siempre los 3 comandos; FreeCAD los registra en setup)."""
    import FreeCAD as App

    workbench.appendMenu("DAV", list(_DAV_TOOLBAR_COMMANDS))
    workbench.appendToolbar("DAV", list(_DAV_TOOLBAR_COMMANDS))
    App.Console.PrintMessage(
        "[DAV] Barra DAV: Preferencias, Iniciar voz, Detener voz. "
        "Si no la ves: workbench DAV + Ver > Barras de herramientas > DAV.\n"
    )


def install_gui_integration() -> None:
    """Carga GUIFreeCad: comandos de voz, tema y extension de la barra DAV."""
    import FreeCAD as App

    dav_commands = importlib.import_module("scr.gui.dav_commands")
    dav_commands._ensure_gui_path()
    from integration.apply_settings import apply_saved_settings

    apply_saved_settings()


def setup_workbench(workbench) -> None:
    """Registra comandos y menu. Sin abrir preferencias al arranque."""
    import FreeCAD as App

    setup_mod_path()
    try:
        dav_commands = importlib.import_module("scr.gui.dav_commands")
        dav_commands.register_commands()
        try:
            install_gui_integration()
        except Exception:
            App.Console.PrintError("[DAV] No se pudo cargar GUIFreeCad (barra incompleta):\n")
            App.Console.PrintError(traceback.format_exc())
        apply_dav_toolbar(workbench)
        _schedule_autoload_workbench()
        _schedule_dav_ui_bootstrap()
        _schedule_toolbar_refresh()
    except Exception:
        App.Console.PrintError("[DAV] Error al inicializar workbench:\n")
        App.Console.PrintError(traceback.format_exc())


def _schedule_autoload_workbench() -> None:
    """Activa workbench DAV al abrir FreeCAD (complementa InitGui.py)."""
    if os.environ.get("DAV_AUTOLOAD_WORKBENCH") != "1":
        return
    try:
        from PySide6.QtCore import QTimer
    except ImportError:
        from PySide2.QtCore import QTimer  # type: ignore[no-redef]

    def _activate() -> None:
        import FreeCADGui as Gui

        try:
            Gui.activateWorkbench("DAVWorkbench")
        except Exception:
            pass

    QTimer.singleShot(400, _activate)


def _schedule_dav_ui_bootstrap() -> None:
    if os.environ.get("DAV_AUTOLOAD_WORKBENCH") != "1":
        return
    try:
        from PySide6.QtCore import QTimer
    except ImportError:
        from PySide2.QtCore import QTimer  # type: ignore[no-redef]

    def _apply_ui() -> None:
        try:
            dav_commands = importlib.import_module("scr.gui.dav_commands")
            dav_commands._ensure_gui_path()
            from integration.freecad_ui_setup import apply_dav_freecad_ui

            apply_dav_freecad_ui()
        except Exception:
            import FreeCAD as App

            App.Console.PrintWarning("[DAV] No se pudo aplicar ajustes de ventana.\n")

    QTimer.singleShot(250, _apply_ui)


def _schedule_toolbar_refresh() -> None:
    """Reaplica la barra DAV tras activar el workbench (evita barra vacia)."""
    try:
        from PySide6.QtCore import QTimer
    except ImportError:
        from PySide2.QtCore import QTimer  # type: ignore[no-redef]

    def _refresh() -> None:
        import FreeCAD as App
        import FreeCADGui as Gui

        try:
            try:
                install_gui_integration()
            except Exception:
                App.Console.PrintError("[DAV] Reintento GUIFreeCad fallo:\n")
                App.Console.PrintError(traceback.format_exc())
            wb = Gui.getWorkbench("DAVWorkbench")
            if wb is not None:
                apply_dav_toolbar(wb)
        except Exception:
            App.Console.PrintError("[DAV] Error refrescando barra DAV:\n")
            App.Console.PrintError(traceback.format_exc())

    for delay_ms in (600, 1500):
        QTimer.singleShot(delay_ms, _refresh)

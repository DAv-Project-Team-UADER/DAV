"""Logica del workbench DAV (importado como modulo Python normal)."""

from __future__ import annotations

import importlib
import os
import sys
import traceback


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


def setup_workbench(workbench) -> None:
    """Registra comandos y menu. Sin abrir preferencias al arranque."""
    import FreeCAD as App

    setup_mod_path()
    try:
        dav_commands = importlib.import_module("scr.gui.dav_commands")
        dav_commands.register_commands()
        workbench.appendMenu("DAV", ["DAV_OpenPreferences"])
        workbench.appendToolbar("DAV", ["DAV_OpenPreferences"])
        _apply_saved_theme()
        _schedule_dav_ui_bootstrap()
    except Exception:
        App.Console.PrintError("[DAV] Error al inicializar workbench:\n")
        App.Console.PrintError(traceback.format_exc())


def _apply_saved_theme() -> None:
    """Aplica tema guardado sin abrir el dialogo."""
    try:
        dav_commands = importlib.import_module("scr.gui.dav_commands")
        dav_commands._ensure_gui_path()
        from integration.apply_settings import apply_saved_settings

        apply_saved_settings()
    except Exception:
        pass


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
            pass

    QTimer.singleShot(250, _apply_ui)

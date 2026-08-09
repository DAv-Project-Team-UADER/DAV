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
        dav_commands._ensure_selection_path()
        dav_commands._ensure_validation_path()
        dav_commands.register_commands()
        try:
            install_gui_integration()
        except Exception:
            App.Console.PrintError("[DAV] No se pudo cargar GUIFreeCad (barra incompleta):\n")
            App.Console.PrintError(traceback.format_exc())
        apply_dav_toolbar(workbench)
        _schedule_autoload_workbench()
        _schedule_dav_ui_bootstrap()
        _schedule_interfaz_dav_launch()
        _schedule_toolbar_refresh()
        _schedule_report_view()
        _schedule_settings_watcher()
    except Exception:
        App.Console.PrintError("[DAV] Error al inicializar workbench:\n")
        App.Console.PrintError(traceback.format_exc())


def _schedule_autoload_workbench() -> None:
    """Activa workbench DAV al abrir FreeCAD (complementa InitGui.py)."""
    if os.environ.get("DAV_AUTOLOAD_WORKBENCH") == "0":
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
    if os.environ.get("DAV_AUTOLOAD_WORKBENCH") == "0":
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


def _schedule_interfaz_dav_launch() -> None:
    """Lanza la interfaz grafica flotante de DAV (InterfazDAV/main.py)."""
    if os.environ.get("DAV_AUTO_LAUNCH_INTERFAZ") == "0":
        return
    try:
        from PySide6.QtCore import QTimer
    except ImportError:
        from PySide2.QtCore import QTimer  # type: ignore[no-redef]

    def _launch() -> None:
        try:
            dav_commands = importlib.import_module("scr.gui.dav_commands")
            dav_commands._launch_interfaz_dav()
        except Exception:
            import FreeCAD as App

            App.Console.PrintWarning("[DAV] No se pudo lanzar la InterfazDAV automatica.\n")

    QTimer.singleShot(800, _launch)


def _force_show_dav_toolbar() -> None:
    """Force-show the DAV toolbar via Qt (survives FreeCAD toolbar-hide memory)."""
    try:
        import FreeCADGui as Gui

        mw = Gui.getMainWindow()
        if mw is None:
            return
        try:
            from PySide6.QtWidgets import QToolBar
        except ImportError:
            from PySide2.QtWidgets import QToolBar  # type: ignore[no-redef]
        for tb in mw.findChildren(QToolBar):
            if tb.windowTitle() == "DAV":
                tb.setVisible(True)
                tb.setEnabled(True)
                break
    except Exception:
        pass


def _auto_start_voice_if_needed() -> None:
    """Start voice automatically when the workbench loads if auto_voice is set."""
    try:
        import sys
        from pathlib import Path

        _dav_commands = importlib.import_module("scr.gui.dav_commands")
        gui_root = _dav_commands._guifreecad_root()
        if str(gui_root) not in sys.path:
            sys.path.insert(0, str(gui_root))

        from core.settings import settings

        settings.load()
        if not (os.environ.get("DAV_AUTO_START_VOICE") == "1" or settings.auto_voice or settings.startup_enabled):
            return

        from integration.voice_bootstrap import start_voice_engine

        start_voice_engine()
        # InterfazDAV launch handled by _schedule_interfaz_dav_launch()
    except Exception:
        pass


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
            _force_show_dav_toolbar()
        except Exception:
            App.Console.PrintError("[DAV] Error refrescando barra DAV:\n")
            App.Console.PrintError(traceback.format_exc())

    def _refresh_and_autovoice() -> None:
        _refresh()
        _auto_start_voice_if_needed()

    for delay_ms in (600, 1500):
        QTimer.singleShot(delay_ms, _refresh)
    QTimer.singleShot(2000, _auto_start_voice_if_needed)


def _schedule_report_view() -> None:
    try:
        from PySide6.QtCore import QTimer
    except ImportError:
        from PySide2.QtCore import QTimer  # type: ignore[no-redef]

    def _show() -> None:
        try:
            import FreeCADGui as Gui
            try:
                from PySide6.QtWidgets import QDockWidget
            except ImportError:
                from PySide2.QtWidgets import QDockWidget  # type: ignore[no-redef]
            mw = Gui.getMainWindow()
            if mw is None:
                return
            for dock in mw.findChildren(QDockWidget):
                if dock.objectName() in ("Std_ReportView", "Report view", "Informe"):
                    dock.show()
                    dock.raise_()
                    return
            Gui.runCommand("Std_ReportView", 0)
        except Exception:
            pass

    QTimer.singleShot(1000, _show)


def _schedule_settings_watcher() -> None:
    """Watch IntegracionGUI settings.json so changes from InterfazDAV apply to FreeCAD."""
    try:
        from PySide6.QtCore import QTimer
    except ImportError:
        from PySide2.QtCore import QTimer  # type: ignore[no-redef]

    def _setup() -> None:
        try:
            import json
            import FreeCAD as App
            try:
                from PySide6.QtWidgets import QApplication
            except ImportError:
                from PySide2.QtWidgets import QApplication  # type: ignore[no-redef]

            from pathlib import Path
            here = Path(__file__).resolve()
            settings_path = None
            for ancestor in here.parents:
                candidate = ancestor / "IntegracionGUI" / "GUIFreeCad" / "config" / "settings.json"
                if candidate.exists():
                    settings_path = candidate
                    break
            if settings_path is None:
                settings_path = here.parents[3] / "IntegracionGUI" / "GUIFreeCad" / "config" / "settings.json"

            last_mtime: list[float] = [settings_path.stat().st_mtime if settings_path.exists() else 0.0]

            def _poll() -> None:
                try:
                    mtime = settings_path.stat().st_mtime if settings_path.exists() else 0.0
                    if mtime == last_mtime[0]:
                        return
                    last_mtime[0] = mtime
                    with open(settings_path, encoding="utf-8") as fh:
                        data = json.load(fh)
                    app = QApplication.instance()
                    if app is not None:
                        dav_cmds = importlib.import_module("scr.gui.dav_commands")
                        dav_cmds._ensure_gui_path()
                        from ui.theme import apply_theme
                        apply_theme(app, data.get("theme", "light"))
                    App.Console.PrintMessage(
                        f"[DAV] Preferencias actualizadas "
                        f"(idioma={data.get('language','?')}, tema={data.get('theme','?')}).\n"
                    )
                except Exception:
                    pass

            poll_timer = QTimer()
            poll_timer.timeout.connect(_poll)
            poll_timer.start(1000)
            App.__dav_settings_poll_timer = poll_timer  
        except Exception:
            pass

    QTimer.singleShot(1500, _setup)

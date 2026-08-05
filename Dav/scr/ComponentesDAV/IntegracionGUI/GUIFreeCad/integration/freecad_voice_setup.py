"""Register DAV voice commands and hooks from GUIFreeCad (minimal touch to PruebaIntegracion)."""

from __future__ import annotations

import os
import subprocess
import traceback
from pathlib import Path

_INSTALLED = False


def install_freecad_integration() -> None:
    """Called from apply_saved_settings when the DAV workbench loads."""
    global _INSTALLED
    if _INSTALLED:
        _maybe_autostart_voice()
        return

    try:
        import FreeCAD as App
        import FreeCADGui as Gui

        from integration.dav_paths import ensure_gui_on_path
        from integration.freecad_gui_bridge import init_gui_bridge

        ensure_gui_on_path()
        init_gui_bridge()
        _register_voice_commands(Gui)
        _extend_workbench_ui(Gui)
        _INSTALLED = True

        App.Console.PrintMessage(
            "[DAV] Workbench listo. Mensajes [DAV] van a esta pestaña «Informe», "
            "no a la consola Python (>>>).\n"
        )
        _print_voice_startup_hint()
        _maybe_autostart_voice()
    except Exception:
        try:
            import FreeCAD as App

            App.Console.PrintError("[DAV] Error instalando integración GUIFreeCad:\n")
            App.Console.PrintError(traceback.format_exc())
        except ImportError:
            pass


def _register_voice_commands(Gui) -> None:
    class _StartVoice:
        def GetResources(self):
            return {
                "Pixmap": "media-playback-start",
                "MenuText": "Iniciar voz DAV",
                "ToolTip": "Activa comandos de voz CAD (motor unificado GUIFreeCad)",
            }

        def Activated(self):
            from integration.voice_bootstrap import start_voice_engine

            start_voice_engine()
            _launch_interfaz_dav()

        def IsActive(self):
            return True

    class _StopVoice:
        def GetResources(self):
            return {
                "Pixmap": "media-playback-stop",
                "MenuText": "Detener voz DAV",
                "ToolTip": "Detiene el motor de comandos por voz",
            }

        def Activated(self):
            from integration.voice_bootstrap import stop_voice_engine

            stop_voice_engine()

        def IsActive(self):
            return True

    for cmd_id, factory in (
        ("DAV_StartVoice", _StartVoice),
        ("DAV_StopVoice", _StopVoice),
    ):
        if Gui.listCommands().count(cmd_id) == 0:
            Gui.addCommand(cmd_id, factory())


def _extend_workbench_ui(Gui) -> None:
    try:
        wb = Gui.getWorkbench("DAVWorkbench")
    except Exception:
        return
    if wb is None:
        return
    cmds = [
        c
        for c in ("DAV_OpenPreferences", "DAV_StartVoice", "DAV_StopVoice")
        if Gui.listCommands().count(c) > 0
    ]
    if not cmds:
        return
    try:
        wb.appendMenu("DAV", cmds)
        wb.appendToolbar("DAV", cmds)
    except Exception:
        import traceback

        import FreeCAD as App

        App.Console.PrintWarning("[DAV] No se pudo actualizar menu/barra DAV:\n")
        App.Console.PrintWarning(traceback.format_exc())


def _print_voice_startup_hint() -> None:
    try:
        import FreeCAD as App
        from core.settings import settings

        settings.load()
        auto = os.environ.get("DAV_AUTO_START_VOICE") == "1" or settings.startup_enabled
        if auto:
            App.Console.PrintMessage(
                "[DAV] Arranque de voz programado (~1,5 s). Esperá «Voz activa» en Informe.\n"
            )
        else:
            App.Console.PrintMessage(
                "[DAV] Micrófono inactivo. Activá «Iniciar DAV y FreeCAD al encender la PC» "
                "en Preferencias, o clic en «Iniciar voz DAV».\n"
            )
    except Exception:
        pass


def _launch_interfaz_dav() -> None:
    try:
        from integration.dav_paths import dav_repo_root

        repo_root = dav_repo_root()
        script = repo_root / "ComponentesDAV" / "InterfazDAV" / "main.py"
        if not script.exists():
            return
        gui_root = repo_root / "ComponentesDAV" / "IntegracionGUI" / "GUIFreeCad"
        python = ""
        for candidate in (
            gui_root / ".venv" / "Scripts" / "pythonw.exe",
            gui_root / ".venv" / "Scripts" / "python.exe",
        ):
            if candidate.exists():
                python = str(candidate)
                break
        if not python:
            python = (
                os.environ.get("PYTHONEXECUTABLE", "").strip()
                or os.environ.get("PYTHON", "").strip()
                or "pythonw"
            )
        env = os.environ.copy()
        env["DAV_PASSIVE_HISTORY_VIEWER"] = "1"
        subprocess.Popen([python, str(script)], cwd=str(script.parent), env=env)
    except Exception:
        try:
            import FreeCAD as App

            App.Console.PrintWarning("[DAV] No se pudo abrir la ventana de historial.\n")
        except ImportError:
            pass


def _maybe_autostart_voice() -> None:
    try:
        import os

        import FreeCAD as App
        from core.settings import settings

        settings.load()
        if not (os.environ.get("DAV_AUTO_START_VOICE") == "1" or settings.startup_enabled):
            return

        try:
            from PySide6.QtCore import QTimer
        except ImportError:
            from PySide2.QtCore import QTimer  # type: ignore[no-redef]

        def _start() -> None:
            from integration.voice_bootstrap import start_voice_engine

            if not start_voice_engine():
                App.Console.PrintWarning(
                    "[DAV] No se pudo iniciar la voz. "
                    "Probá «Iniciar voz DAV» manualmente.\n"
                )

        QTimer.singleShot(1500, _start)
    except Exception:
        try:
            import FreeCAD as App

            App.Console.PrintError("[DAV] Error programando arranque de voz:\n")
            App.Console.PrintError(traceback.format_exc())
        except ImportError:
            pass

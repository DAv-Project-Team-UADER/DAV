"""Register DAV voice commands and hooks from GUIFreeCad (minimal touch to PruebaIntegracion)."""

from __future__ import annotations

import os
import traceback

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
    try:
        wb.appendMenu("DAV", ["DAV_OpenPreferences", "DAV_StartVoice", "DAV_StopVoice"])
        wb.appendToolbar("DAV", ["DAV_OpenPreferences", "DAV_StartVoice", "DAV_StopVoice"])
    except Exception:
        pass


def _print_voice_startup_hint() -> None:
    try:
        import FreeCAD as App
        from core.settings import settings

        settings.load()
        auto = os.environ.get("DAV_AUTO_START_VOICE") == "1" or settings.startup_enabled
        if auto:
            App.Console.PrintMessage(
                "[DAV] Arranque de voz programado (~1 s). Esperá «Voz activa» en Informe.\n"
            )
        else:
            App.Console.PrintMessage(
                "[DAV] Micrófono inactivo. Clic en «Iniciar voz DAV» en la barra DAV.\n"
            )
    except Exception:
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

"""FreeCAD commands that bridge to GUIFreeCad."""

from __future__ import annotations

import os
import sys
from pathlib import Path


def _dav_repo_root() -> Path | None:
    mod = os.environ.get("DAV_MOD_ROOT", "").strip()
    if mod:
        mod_path = Path(mod).resolve()
        if mod_path.name.upper() == "DAV":
            return mod_path.parent
    try:
        here = Path(__file__).resolve()
        if here.parents[2].name.upper() == "DAV":
            return here.parents[3]
    except (IndexError, NameError):
        pass
    return None


def _guifreecad_root() -> Path:
    env = os.environ.get("DAV_GUI_FREECAD_ROOT", "").strip()
    if env:
        path = Path(env)
        if path.is_dir():
            return path

    repo = _dav_repo_root()
    if repo is not None:
        for candidate in (
            repo / "luigiIntegracionV1" / "GUIFreeCad",
            repo / "GUIFreeCad",
        ):
            if candidate.is_dir():
                return candidate

    try:
        here = Path(__file__).resolve()
        sibling = here.parents[5] / "GUIFreeCad"
        if sibling.is_dir():
            return sibling
    except (IndexError, NameError):
        pass

    return Path(env) if env else Path(".")


def _ensure_gui_path() -> Path:
    root = _guifreecad_root()
    text = str(root)
    if not root.is_dir():
        raise FileNotFoundError(
            f"No se encontro GUIFreeCad en '{root}'. "
            "Usa iniciar_dav.bat o define DAV_GUI_FREECAD_ROOT."
        )
    if text not in sys.path:
        sys.path.insert(0, text)
    return root


class DAV_OpenPreferencesCommand:
    def GetResources(self):
        return {
            "Pixmap": "preferences-general",
            "MenuText": "Preferencias DAV",
            "ToolTip": "Configuracion DAV (idioma, voz, tema)",
        }

    def Activated(self):
        _ensure_gui_path()
        from integration.launch_preferences import open_preferences

        open_preferences()

    def IsActive(self):
        return True


class DAV_StartVoiceCommand:
    def GetResources(self):
        return {
            "Pixmap": "media-playback-start",
            "MenuText": "Iniciar voz DAV",
            "ToolTip": "Activa comandos de voz CAD (GUIFreeCad)",
        }

    def Activated(self):
        _ensure_gui_path()
        from integration.voice_bootstrap import start_voice_engine

        start_voice_engine()
        _launch_interfaz_dav()

    def IsActive(self):
        return True


class DAV_StopVoiceCommand:
    def GetResources(self):
        return {
            "Pixmap": "media-playback-stop",
            "MenuText": "Detener voz DAV",
            "ToolTip": "Detiene el motor de comandos por voz",
        }

    def Activated(self):
        _ensure_gui_path()
        from integration.voice_bootstrap import stop_voice_engine

        stop_voice_engine()

    def IsActive(self):
        return True


_interfaz_proc = None


def _find_system_python() -> str:
    import subprocess as _sp

    gui_root_env = os.environ.get("DAV_GUI_FREECAD_ROOT", "").strip()
    if gui_root_env:
        venv_py = Path(gui_root_env) / ".venv" / "Scripts" / "python.exe"
        if venv_py.exists():
            return str(venv_py)

    for cmd in (["py", "-3"], ["python3"], ["python"]):
        try:
            out = _sp.check_output(
                cmd + ["-c", "import sys; print(sys.executable)"],
                stderr=_sp.DEVNULL,
                timeout=3,
            ).decode().strip()
            if out and Path(out).exists():
                return out
        except Exception:
            pass

    import sys as _sys
    return _sys.executable


def _launch_interfaz_dav() -> None:
    global _interfaz_proc
    import subprocess

    repo = _dav_repo_root()
    if repo is None:
        return
    script = repo / "InterfazDAV" / "main.py"
    if not script.exists():
        try:
            import FreeCAD as App
            App.Console.PrintWarning(f"[DAV] InterfazDAV no encontrado en: {script}\n")
        except ImportError:
            print(f"[DAV] InterfazDAV no encontrado en: {script}")
        return
    if _interfaz_proc is not None and _interfaz_proc.poll() is None:
        try:
            import FreeCAD as App
            App.Console.PrintMessage("[DAV] InterfazDAV ya esta corriendo.\n")
        except ImportError:
            print("[DAV] InterfazDAV ya esta corriendo.")
        return
    python = _find_system_python()
    bat_path = script.parent / "run_interfaz.bat"
    
    try:
        with open(bat_path, "w", encoding="utf-8") as f:
            f.write(f'@echo off\n')
            f.write(f'cd /d "{script.parent}"\n')
            f.write(f'"{python}" "{script}"\n')
            f.write(f'pause\n')
    except Exception as e:
        try:
            import FreeCAD as App
            App.Console.PrintError(f"[DAV] No se pudo crear el archivo batch: {e}\n")
        except ImportError:
            print(f"[DAV] No se pudo crear el archivo batch: {e}")
        return

    import subprocess
    _interfaz_proc = subprocess.Popen(
        ["explorer.exe", str(bat_path)]
    )


def register_commands() -> None:
    import FreeCADGui as Gui

    for cmd_id, factory in (
        ("DAV_OpenPreferences", DAV_OpenPreferencesCommand),
        ("DAV_StartVoice", DAV_StartVoiceCommand),
        ("DAV_StopVoice", DAV_StopVoiceCommand),
    ):
        if Gui.listCommands().count(cmd_id) == 0:
            Gui.addCommand(cmd_id, factory())

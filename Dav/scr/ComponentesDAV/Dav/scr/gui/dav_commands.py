"""FreeCAD commands that bridge to GUIFreeCad."""

from __future__ import annotations

import os
import sys
from pathlib import Path


def _dav_repo_root() -> Path | None:
    mod = os.environ.get("DAV_MOD_ROOT", "").strip()
    if mod:
        mod_path = Path(mod).resolve()
        if mod_path.is_file():
            mod_path = mod_path.parent
        if mod_path.name.upper() == "DAV":
            return mod_path.parent
    try:
        here = Path(__file__).resolve()
        # ComponentesDAV tiene prioridad: al subir ancestros aparece "Dav"
        # antes que "ComponentesDAV", así que se busca primero el repo de
        # componentes en toda la cadena y solo se cae a "DAV" si no aparece.
        for ancestor in here.parents:
            if ancestor.name.upper() == "COMPONENTESDAV":
                return ancestor
        for ancestor in here.parents:
            if ancestor.name.upper() == "DAV":
                return ancestor
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
            repo / "IntegracionGUI" / "GUIFreeCad",
            repo / "componentesDAV" / "IntegracionGUI" / "GUIFreeCad",
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
    parent_text = str(root.parent)
    if parent_text not in sys.path:
        sys.path.insert(0, parent_text)
    return root


def _selection_root() -> Path:
    env = os.environ.get("DAV_SELECTION_ROOT", "").strip()
    if env:
        path = Path(env)
        if path.is_dir():
            return path.resolve()

    repo = _dav_repo_root()
    for candidate in _selection_candidates(repo):
        if candidate.is_dir():
            return candidate.resolve()

    try:
        here = Path(__file__).resolve()
        for ancestor in here.parents:
            candidate = ancestor / "selection"
            if candidate.is_dir() and (candidate / "tagger.py").is_file():
                return candidate.resolve()
    except (IndexError, NameError):
        pass

    return Path(".")


def _selection_candidates(repo: Path | None) -> tuple[Path, ...]:
    if repo is None:
        return ()
    return (
        repo / "selection",
        repo.parent / "selection",
    )


def _ensure_selection_path() -> Path:
    root = _selection_root()
    text = str(root)
    if root.is_dir() and text not in sys.path:
        sys.path.insert(0, text)
    return root


def RunAlexSelectionPrueba(sketch_name: str | None = None):
    """
    Prueba completa selection/ para consola FreeCAD (sin configurar rutas).

    Uso tras git pull + iniciar_dav.bat:
        from scr.gui.dav_commands import RunAlexSelectionPrueba
        selector = RunAlexSelectionPrueba()
        selector.SelectOther = True
    """
    _ensure_selection_path()
    from prueba_alex import RunFullDemo

    return RunFullDemo(sketch_name=sketch_name)


def _validation_root() -> Path:
    env = os.environ.get("DAV_VALIDATION_ROOT", "").strip()
    if env:
        path = Path(env)
        if path.is_dir():
            return path.resolve()

    repo = _dav_repo_root()
    for candidate in _validation_candidates(repo):
        if candidate.is_dir():
            return candidate.resolve()

    try:
        here = Path(__file__).resolve()
        for ancestor in here.parents:
            candidate = ancestor / "validation"
            if candidate.is_dir() and (candidate / "validator.py").is_file():
                return candidate.resolve()
    except (IndexError, NameError):
        pass

    return Path(".")


def _validation_candidates(repo: Path | None) -> tuple[Path, ...]:
    if repo is None:
        return ()
    return (
        repo / "validation",
        repo.parent / "validation",
    )


def _dictionary_root() -> Path:
    env = os.environ.get("DAV_DICTIONARY_ROOT", "").strip()
    if env:
        path = Path(env)
        if path.is_dir():
            return path.resolve()

    repo = _dav_repo_root()
    for candidate in _dictionary_candidates(repo):
        if candidate.is_dir():
            return candidate.resolve()

    try:
        here = Path(__file__).resolve()
        for ancestor in here.parents:
            candidate = ancestor / "DiccionariosEnBruto"
            if candidate.is_dir():
                return candidate.resolve()
    except (IndexError, NameError):
        pass

    return Path("DiccionariosEnBruto")


def _dictionary_candidates(repo: Path | None) -> tuple[Path, ...]:
    if repo is None:
        return ()
    return (
        repo / "DiccionariosEnBruto",
        repo.parent / "DiccionariosEnBruto",
    )


def _ensure_validation_path() -> Path:
    root = _validation_root()
    text = str(root)
    if root.is_dir() and text not in sys.path:
        sys.path.insert(0, text)

    dic = _dictionary_root()
    dic_text = str(dic)
    if dic.is_dir() and dic_text not in sys.path:
        sys.path.insert(0, dic_text)
    return root


def RunValidatorPrueba(sketch_name: str = "Sketch") -> None:
    """
    Demo Validator en consola FreeCAD (sin configurar rutas).

    Uso tras git pull + iniciar_dav.bat:
        from scr.gui.dav_commands import RunValidatorPrueba
        RunValidatorPrueba()
    """
    _ensure_validation_path()
    from prueba_validator import RunFullDemo

    RunFullDemo(sketch_name=sketch_name)


def _show_report_view() -> None:
    try:
        import FreeCADGui as Gui
        from PySide6.QtWidgets import QDockWidget
        mw = Gui.getMainWindow()
        if mw is None:
            return
        for dock in mw.findChildren(QDockWidget):
            if dock.objectName() in ("Std_ReportView", "Report view", "Informe"):
                dock.show()
                dock.raise_()
                return
        # Fallback: use FreeCAD command to open it
        Gui.runCommand("Std_ReportView", 0)
    except Exception:
        pass


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


def _find_pythonw(python_path: str) -> str:
    p = Path(python_path)
    candidate = p.parent / "pythonw.exe"
    return str(candidate) if candidate.exists() else python_path


_INTERFAZ_WINDOW_TITLE = "Asistente de Voz - Control por Comandos"


def _bring_interfaz_to_front() -> bool:
    try:
        import ctypes
        hwnd = ctypes.windll.user32.FindWindowW(None, _INTERFAZ_WINDOW_TITLE)
        if hwnd:
            ctypes.windll.user32.ShowWindow(hwnd, 9)   # SW_RESTORE
            ctypes.windll.user32.SetForegroundWindow(hwnd)
            return True
    except Exception:
        pass
    return False


def _launch_interfaz_dav() -> None:
    global _interfaz_proc
    import subprocess

    repo = _dav_repo_root()
    if repo is None:
        return
    script = repo / "InterfazDAV" / "main.py"
    if not script.exists():
        script = repo / "componentesDAV" / "InterfazDAV" / "main.py"
    if not script.exists():
        try:
            import FreeCAD as App
            App.Console.PrintWarning(f"[DAV] InterfazDAV no encontrado en: {script}\n")
        except ImportError:
            print(f"[DAV] InterfazDAV no encontrado en: {script}")
        return
    if _bring_interfaz_to_front():
        try:
            import FreeCAD as App
            App.Console.PrintMessage("[DAV] InterfazDAV ya esta corriendo — traida al frente.\n")
        except ImportError:
            print("[DAV] InterfazDAV ya esta corriendo — traida al frente.")
        return
    python = _find_system_python()
    pythonw = _find_pythonw(python)
    bat_path = script.parent / "run_interfaz.bat"
    try:
        with open(bat_path, "w", encoding="utf-8") as f:
            f.write('@echo off\n')
            f.write(f'cd /d "{script.parent}"\n')
            f.write(f'start "" "{pythonw}" "{script}"\n')
    except Exception as e:
        try:
            import FreeCAD as App
            App.Console.PrintError(f"[DAV] No se pudo crear el bat: {e}\n")
        except ImportError:
            print(f"[DAV] No se pudo crear el bat: {e}")
        return
    _interfaz_proc = subprocess.Popen(["explorer.exe", str(bat_path)])


def register_commands() -> None:
    import FreeCADGui as Gui

    for cmd_id, factory in (
        ("DAV_OpenPreferences", DAV_OpenPreferencesCommand),
        ("DAV_StartVoice", DAV_StartVoiceCommand),
        ("DAV_StopVoice", DAV_StopVoiceCommand),
    ):
        if Gui.listCommands().count(cmd_id) == 0:
            Gui.addCommand(cmd_id, factory())

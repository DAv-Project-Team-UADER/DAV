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
        if _is_dictionary_dir(candidate):
            return candidate.resolve()

    try:
        here = Path(__file__).resolve()
        for ancestor in here.parents:
            for candidate in (ancestor / "Dav" / "dic", ancestor / "DiccionariosEnBruto"):
                if _is_dictionary_dir(candidate):
                    return candidate.resolve()
    except (IndexError, NameError):
        pass

    return Path("DiccionariosEnBruto")


def _is_dictionary_dir(path: Path) -> bool:
    """True si la carpeta es un diccionario real (no un placeholder vacío).

    Evita confundir ``ComponentesDAV/Dav/dic`` (solo placeholder) con el
    ``Dav/dic`` real que contiene base.py y los TraduceTo*.py.
    """
    return (path / "base.py").is_file() or (path / "TraduceToEs.py").is_file()


def _dictionary_candidates(repo: Path | None) -> tuple[Path, ...]:
    if repo is None:
        return ()
    return (
        # Layout DavCore: los diccionarios viven en Dav/dic.
        repo / "Dav" / "dic",
        repo.parent / "Dav" / "dic",
        # Layout previo (plano en la raíz del repo).
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


class DAV_ShowPanelCommand:
    def GetResources(self):
        return {
            "Pixmap": "Std_DlgCustomize",
            "MenuText": "Mostrar panel DAV",
            "ToolTip": (
                "Muestra el panel DAV acoplado dentro de FreeCAD "
                "(requiere la voz activa)"
            ),
        }

    def Activated(self):
        _ensure_gui_path()
        from integration.voice_bootstrap import show_dock_panel

        show_dock_panel()

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


_interfaz_proc: subprocess.Popen | None = None
_last_launch_time: float = 0.0


def _venv_python() -> Path | None:
    """Interprete del venv de GUIFreeCad, resuelto por ruta del repo.

    No depende de DAV_GUI_FREECAD_ROOT: ``_guifreecad_root()`` ya localiza la
    carpeta recorriendo el layout, y la variable de entorno sigue teniendo
    prioridad dentro de esa funcion.

    Returns:
        Path al python.exe del venv, o None si no existe.
    """
    try:
        root = _guifreecad_root()
    except Exception:
        return None

    for rel in ((".venv", "Scripts", "python.exe"), (".venv", "bin", "python")):
        candidate = root.joinpath(*rel)
        if candidate.is_file():
            return candidate
    return None


def _has_pyside6(python_path: str) -> bool:
    """True si ese interprete puede importar PySide6.

    La InterfazDAV es una app PySide6: un interprete sin PySide6 arranca y
    muere al primer import. Como se lanza con pythonw (sin consola), el
    ModuleNotFoundError no se ve en ningun lado, asi que conviene descartarlo
    antes de intentar.
    """
    import subprocess as _sp

    try:
        return _sp.call(
            [python_path, "-c", "import PySide6"],
            stdout=_sp.DEVNULL,
            stderr=_sp.DEVNULL,
            timeout=15,
        ) == 0
    except Exception:
        return False


def _find_system_python() -> str:
    """Interprete para lanzar la InterfazDAV, priorizando el venv del repo.

    Orden: venv de GUIFreeCad → interpretes del sistema que tengan PySide6 →
    el primer interprete encontrado (aunque no sirva, para que el llamador
    reporte un error concreto en vez de no hacer nada).
    """
    import subprocess as _sp

    venv_py = _venv_python()
    if venv_py is not None:
        return str(venv_py)

    fallback = ""
    for cmd in (["py", "-3"], ["python3"], ["python"]):
        try:
            out = _sp.check_output(
                cmd + ["-c", "import sys; print(sys.executable)"],
                stderr=_sp.DEVNULL,
                timeout=3,
            ).decode().strip()
            if not out or not Path(out).exists():
                continue
            if _has_pyside6(out):
                return out
            fallback = fallback or out
        except Exception:
            pass

    if fallback:
        return fallback

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


def close_interfaz_dav() -> None:
    global _interfaz_proc
    if _interfaz_proc is not None and _interfaz_proc.poll() is None:
        try:
            _interfaz_proc.terminate()
        except Exception:
            pass
        _interfaz_proc = None


def _launch_interfaz_dav() -> None:
    global _interfaz_proc, _last_launch_time
    import os
    import time
    import subprocess

    now = time.time()
    if _interfaz_proc is not None and _interfaz_proc.poll() is None:
        _bring_interfaz_to_front()
        return

    if now - _last_launch_time < 3.0:
        return

    if _bring_interfaz_to_front():
        return

    _last_launch_time = now

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

    python = _find_system_python()
    pythonw = _find_pythonw(python)

    if not _has_pyside6(python):
        _report(
            f"[DAV] El interprete '{python}' no tiene PySide6, la InterfazDAV no "
            f"puede arrancar.\n"
            f"[DAV] Instalalo con: \"{python}\" -m pip install PySide6\n",
            error=True,
        )
        return

    env = os.environ.copy()
    env["DAV_PASSIVE_HISTORY_VIEWER"] = "1"
    env["DAV_FREECAD_PID"] = str(os.getpid())

    # pythonw no tiene consola: si main.py falla al importar, el proceso muere
    # sin dejar rastro. Se captura stderr para poder reportar el motivo.
    try:
        _interfaz_proc = subprocess.Popen(
            [pythonw, str(script)],
            cwd=str(script.parent),
            env=env,
            stderr=subprocess.PIPE,
        )
    except Exception as e:
        _report(f"[DAV] No se pudo lanzar InterfazDAV: {e}\n", error=True)
        return

    # Popen tiene exito aunque el script muera al primer import, asi que hay
    # que mirar el proceso un instante despues para saber si sobrevivio.
    _check_interfaz_started(_interfaz_proc)


def _report(message: str, *, error: bool = False) -> None:
    """Escribe en la consola de FreeCAD, o en stdout fuera de FreeCAD."""
    try:
        import FreeCAD as App
        if error:
            App.Console.PrintError(message)
        else:
            App.Console.PrintWarning(message)
    except ImportError:
        print(message, end="")


def _check_interfaz_started(proc: "subprocess.Popen") -> None:
    """Verifica que la InterfazDAV siga viva y reporta el stderr si murio.

    Se llama en diferido (1,5 s) para no bloquear la UI de FreeCAD. Si el
    proceso ya termino, lee lo que dejo en stderr y lo publica en la consola:
    sin esto, un fallo de arranque bajo pythonw es completamente invisible.
    """
    def _check() -> None:
        if proc.poll() is None:
            return
        detail = ""
        try:
            if proc.stderr is not None:
                detail = proc.stderr.read().decode("utf-8", errors="replace").strip()
        except Exception:
            pass
        msg = f"[DAV] La InterfazDAV se cerro al arrancar (codigo {proc.returncode}).\n"
        if detail:
            msg += f"[DAV] {detail}\n"
        _report(msg, error=True)

    # Diferido via QTimer solo si hay event loop de Qt corriendo (dentro de
    # FreeCAD). Sin loop el singleShot no dispara nunca y el fallo volveria a
    # ser invisible, asi que en ese caso se espera en un hilo aparte.
    try:
        from PySide6.QtCore import QTimer
        from PySide6.QtWidgets import QApplication
        if QApplication.instance() is not None:
            QTimer.singleShot(1500, _check)
            return
    except ImportError:
        pass

    import threading
    import time as _time

    def _wait_and_check() -> None:
        _time.sleep(1.5)
        _check()

    threading.Thread(target=_wait_and_check, daemon=True).start()


def register_commands() -> None:
    import FreeCADGui as Gui

    for cmd_id, factory in (
        ("DAV_OpenPreferences", DAV_OpenPreferencesCommand),
        ("DAV_StartVoice", DAV_StartVoiceCommand),
        ("DAV_StopVoice", DAV_StopVoiceCommand),
        ("DAV_ShowPanel", DAV_ShowPanelCommand),
    ):
        if Gui.listCommands().count(cmd_id) == 0:
            Gui.addCommand(cmd_id, factory())

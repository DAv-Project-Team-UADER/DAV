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
        from integration.voice_bootstrap import show_dock_panel, start_voice_engine

        if start_voice_engine():
            show_dock_panel()

    def IsActive(self):
        return True


class DAV_ShowPanelCommand:
    def GetResources(self):
        return {
            # Nombre del tema de iconos, como los otros comandos DAV: los
            # identificadores de comando tipo "Std_*" no resuelven a un icono.
            "Pixmap": "view-refresh",
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

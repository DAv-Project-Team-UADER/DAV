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


def _selection_root() -> Path:
    env = os.environ.get("DAV_SELECTION_ROOT", "").strip()
    if env:
        path = Path(env)
        if path.is_dir():
            return path.resolve()

    repo = _dav_repo_root()
    if repo is not None:
        candidate = repo / "selection"
        if candidate.is_dir():
            return candidate.resolve()

    try:
        here = Path(__file__).resolve()
        candidate = here.parents[3] / "selection"
        if candidate.is_dir():
            return candidate.resolve()
    except (IndexError, NameError):
        pass

    return Path(".")


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


def register_commands() -> None:
    import FreeCADGui as Gui

    for cmd_id, factory in (
        ("DAV_OpenPreferences", DAV_OpenPreferencesCommand),
        ("DAV_StartVoice", DAV_StartVoiceCommand),
        ("DAV_StopVoice", DAV_StopVoiceCommand),
    ):
        if Gui.listCommands().count(cmd_id) == 0:
            Gui.addCommand(cmd_id, factory())

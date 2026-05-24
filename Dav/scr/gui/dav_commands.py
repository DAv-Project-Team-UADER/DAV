"""FreeCAD commands that bridge to GUIFreeCad."""

from __future__ import annotations

import os
import sys
from pathlib import Path


def _guifreecad_root() -> Path:
    env = os.environ.get("DAV_GUI_FREECAD_ROOT", "").strip()
    if env:
        path = Path(env)
        if path.is_dir():
            return path
    mod = os.environ.get("DAV_MOD_ROOT", "").strip()
    if mod:
        dav_repo = Path(mod).resolve().parent
        embedded = dav_repo / "GUIFreeCad"
        if embedded.is_dir():
            return embedded
        sibling = dav_repo.parent.parent / "GUIFreeCad"
        if sibling.is_dir():
            return sibling
    try:
        here = Path(__file__).resolve()
        embedded = here.parents[4] / "GUIFreeCad"
        if embedded.is_dir():
            return embedded
        sibling = here.parents[5] / "GUIFreeCad"
        if sibling.is_dir():
            return sibling
    except NameError:
        pass
    return Path(env) if env else Path(".")


def _ensure_gui_path():
    root = _guifreecad_root()
    text = str(root)
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


def register_commands() -> None:
    import FreeCADGui as Gui

    Gui.addCommand("DAV_OpenPreferences", DAV_OpenPreferencesCommand())

"""Resolve GUIFreeCad / DAV repo paths inside FreeCAD."""

from __future__ import annotations

import os
import sys
from pathlib import Path

_GUI_ROOT: Path | None = None
_DAV_REPO_ROOT: Path | None = None


def guifreecad_root() -> Path:
    global _GUI_ROOT
    if _GUI_ROOT is not None:
        return _GUI_ROOT

    env = os.environ.get("DAV_GUI_FREECAD_ROOT", "").strip()
    if env:
        path = Path(env)
        if path.is_dir():
            _GUI_ROOT = path
            return path

    try:
        import FreeCAD as App

        for mod_dir in getattr(App, "__ModDirs__", ()) or ():
            norm = Path(mod_dir).resolve()
            if norm.name.upper() == "DAV":
                dav_repo = norm.parent
                embedded = dav_repo / "GUIFreeCad"
                if embedded.is_dir():
                    _GUI_ROOT = embedded
                    return embedded
                sibling = norm.parent.parent.parent / "GUIFreeCad"
                if sibling.is_dir():
                    _GUI_ROOT = sibling
                    return sibling
    except ImportError:
        pass

    here = Path(__file__).resolve()
    sibling = here.parents[1]
    if sibling.name == "GUIFreeCad" and sibling.is_dir():
        _GUI_ROOT = sibling
        return sibling

    sibling = here.parents[2] / "GUIFreeCad"
    if sibling.is_dir():
        _GUI_ROOT = sibling
        return sibling

    _GUI_ROOT = here.parents[1]
    return _GUI_ROOT


def _find_dav_repo() -> Path | None:
    mod = os.environ.get("DAV_MOD_ROOT", "").strip()
    if mod:
        root = Path(mod).resolve().parent
        if (root / "PruebaIntegracion").is_dir():
            return root

    for base in (guifreecad_root().parent, *guifreecad_root().parents):
        if (base / "PruebaIntegracion").is_dir():
            return base
    return None


def dav_repo_root() -> Path:
    global _DAV_REPO_ROOT
    if _DAV_REPO_ROOT is not None:
        return _DAV_REPO_ROOT

    found = _find_dav_repo()
    if found is not None:
        _DAV_REPO_ROOT = found
        return found

    raise FileNotFoundError("No se encontró el repo DAV (PruebaIntegracion).")


def ensure_gui_on_path() -> Path:
    root = guifreecad_root()
    text = str(root)
    if text not in sys.path:
        sys.path.insert(0, text)
    return root


def ensure_dav_repo_on_path() -> Path:
    ensure_gui_on_path()
    root = dav_repo_root()
    text = str(root)
    if text not in sys.path:
        sys.path.insert(0, text)
    return root

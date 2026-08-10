"""Resolve GUIFreeCad / DAV repo paths inside FreeCAD."""

from __future__ import annotations

import os
import sys
from pathlib import Path

_GUI_ROOT: Path | None = None
_DAV_REPO_ROOT: Path | None = None


_INTEGRATION_DIR = "IntegracionGUI"


def _gui_roots_from_dav_repo(dav_repo: Path) -> list[Path]:
    return [
        dav_repo / _INTEGRATION_DIR / "GUIFreeCad",
        dav_repo / "GUIFreeCad",
    ]


def _first_gui_root(candidates: list[Path]) -> Path | None:
    for path in candidates:
        if path.is_dir():
            return path
    return None


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
                found = _first_gui_root(_gui_roots_from_dav_repo(dav_repo))
                if found is not None:
                    _GUI_ROOT = found
                    return found
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

    for parent in here.parents:
        found = _first_gui_root(_gui_roots_from_dav_repo(parent))
        if found is not None:
            _GUI_ROOT = found
            return found

    _GUI_ROOT = here.parents[1]
    return _GUI_ROOT


# Carpetas que identifican a Dav/scr/ como raíz. Antes se usaba
# "PruebaIntegracion", que se retiró a Dav/docs/prototipos/; se marca por
# "validation" y "selection", que están en el camino activo (el Validator de
# PromptedCommandExecutor y CreateObjects de los diccionarios).
_REPO_MARKERS = ("validation", "selection")


def _is_dav_repo(base: Path) -> bool:
    return any((base / marker).is_dir() for marker in _REPO_MARKERS)


def _find_dav_repo() -> Path | None:
    mod = os.environ.get("DAV_MOD_ROOT", "").strip()
    if mod:
        root = Path(mod).resolve().parent
        if _is_dav_repo(root):
            return root

    for base in (guifreecad_root().parent, *guifreecad_root().parents):
        if _is_dav_repo(base):
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

    raise FileNotFoundError(
        "No se encontró el repo DAV (se buscó "
        f"{' / '.join(_REPO_MARKERS)} en los ancestros)."
    )


def ensure_gui_on_path() -> Path:
    root = guifreecad_root()
    text = str(root)
    if text not in sys.path:
        sys.path.insert(0, text)
    parent_text = str(root.parent)
    if parent_text not in sys.path:
        sys.path.insert(0, parent_text)
    return root


def ensure_dav_repo_on_path() -> Path:
    ensure_gui_on_path()
    root = dav_repo_root()
    text = str(root)
    if text not in sys.path:
        sys.path.insert(0, text)
    return root

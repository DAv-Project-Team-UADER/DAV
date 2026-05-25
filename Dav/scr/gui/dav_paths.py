"""Resolve GUIFreeCad root (launcher should set DAV_GUI_FREECAD_ROOT)."""

from __future__ import annotations

import os
from pathlib import Path

_INTEGRATION_DIR = "luigiIntegracionV1"


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


def _mod_dir() -> Path | None:
    from scr.gui.mod_paths import get_mod_dir

    text = get_mod_dir()
    return Path(text) if text else None


def guifreecad_root() -> Path:
    env = os.environ.get("DAV_GUI_FREECAD_ROOT", "").strip()
    if env:
        path = Path(env)
        if path.is_dir():
            return path

    mod = _mod_dir()
    if mod is not None:
        dav_repo = mod.parent
        found = _first_gui_root(_gui_roots_from_dav_repo(dav_repo))
        if found is not None:
            return found
        sibling = mod.parent.parent.parent / "GUIFreeCad"
        if sibling.is_dir():
            return sibling

    try:
        here = Path(__file__).resolve()
        repo_root = here.parents[4]
        found = _first_gui_root(_gui_roots_from_dav_repo(repo_root))
        if found is not None:
            return found
        dev_root = here.parents[5] / "GUIFreeCad"
        if dev_root.is_dir():
            return dev_root
    except NameError:
        pass

    return Path(env) if env else Path(".")

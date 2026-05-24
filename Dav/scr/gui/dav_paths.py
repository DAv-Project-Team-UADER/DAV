"""Resolve GUIFreeCad root (launcher should set DAV_GUI_FREECAD_ROOT)."""

from __future__ import annotations

import os
from pathlib import Path


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
        embedded = mod.parent / "GUIFreeCad"
        if embedded.is_dir():
            return embedded
        sibling = mod.parent.parent.parent / "GUIFreeCad"
        if sibling.is_dir():
            return sibling

    try:
        here = Path(__file__).resolve()
        repo_root = here.parents[4]
        embedded = repo_root / "GUIFreeCad"
        if embedded.is_dir():
            return embedded
        dev_root = here.parents[5] / "GUIFreeCad"
        if dev_root.is_dir():
            return dev_root
    except NameError:
        pass

    return Path(env) if env else Path(".")

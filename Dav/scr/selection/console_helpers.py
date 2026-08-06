# Copyright (C) 2026 El Equipo del Proyecto DAV
# Copyright (C) 2026 The DAV Project Team
# Universidad Autónoma de Entre Ríos (UADER)
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Helpers for FreeCAD console testing.

No hace falta configurar rutas si abrís FreeCAD con iniciar_dav.bat
(el módulo DAV agrega selection/ a sys.path al iniciar).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path


def _BootstrapPath() -> str:
    """Ensure selection/ is importable. Safe to call multiple times."""
    env = os.environ.get("DAV_SELECTION_ROOT", "").strip()
    if env and Path(env).is_dir():
        folder = str(Path(env).resolve())
    else:
        folder = str(Path(__file__).resolve().parent)

    if folder not in sys.path:
        sys.path.insert(0, folder)
    return folder


_BootstrapPath()


def SetupSelectionPath() -> str:
    """Legacy alias — path is already configured on import."""
    return _BootstrapPath()


def RunCreateObjects(
    object_name: str,
    *,
    Is3D: bool = False,
    Language: str | None = None,
) -> None:
    """Run CreateObjects on the named document object."""
    from createobjects import CreateObjects

    worker = CreateObjects(object_name, Is3D=Is3D, Language=Language)
    worker.Execute()


def RunSelectionDemo():
    """
    Load all document object names and select the first via ObjectSelection.

    Returns the ObjectSelection instance. Cycle with:
        selector.SelectOther = True
    """
    import FreeCAD as App
    from object_selection import ObjectSelection

    doc = App.ActiveDocument
    if doc is None:
        print("Error: no active document.")
        return None

    names = [obj.Name for obj in doc.Objects]
    selector = ObjectSelection()
    selector.VectorSelection(names)
    selector.SelectOther = True
    print("Cycle objects: selector.SelectOther = True")
    return selector


def PrintObjectTree() -> None:
    """Print Name and Label of every object (for test reports)."""
    import FreeCAD as App

    doc = App.ActiveDocument
    if doc is None:
        print("Error: no active document.")
        return

    print("\n--- Object tree ---")
    for obj in doc.Objects:
        label = getattr(obj, "Label", obj.Name)
        print(f"  {obj.Name}  |  Label: {label}")
    print("--- end ---\n")

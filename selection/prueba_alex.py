# Copyright (C) 2026 El Equipo del Proyecto DAV
# Copyright (C) 2026 The DAV Project Team
# Universidad Autónoma de Entre Ríos (UADER)
# SPDX-License-Identifier: GPL-3.0-or-later

"""
Prueba guiada para Alex — se ejecuta desde consola FreeCAD sin configurar rutas.

    from scr.gui.dav_commands import RunAlexSelectionPrueba
    RunAlexSelectionPrueba()
"""

from __future__ import annotations

import sys
from pathlib import Path


def _EnsurePath() -> None:
    """Idempotent: selection/ must already be on sys.path via DAV bootstrap."""
    selection_dir = Path(__file__).resolve().parent
    text = str(selection_dir)
    if text not in sys.path:
        sys.path.insert(0, text)


def _FindSketchName(preferred: str | None) -> str | None:
    import FreeCAD as App

    doc = App.ActiveDocument
    if doc is None:
        print("[DAV] Error: no hay documento activo. Creá uno nuevo (Archivo > Nuevo).")
        return None

    if preferred:
        if doc.getObject(preferred):
            return preferred
        print(f"[DAV] No existe '{preferred}'. Buscando Sketch automáticamente...")

    for obj in doc.Objects:
        type_id = getattr(obj, "TypeId", "")
        if "Sketcher" in type_id or obj.Name.lower().startswith("sketch"):
            print(f"[DAV] Sketch detectado: '{obj.Name}'")
            return obj.Name

    if doc.Objects:
        fallback = doc.Objects[0].Name
        print(f"[DAV] No hay Sketch; uso el primer objeto: '{fallback}'")
        return fallback

    print("[DAV] Documento vacío. Creá un Sketch con al menos 5 herramientas Sketcher.")
    return None


def RunFullDemo(sketch_name: str | None = None):
    """CreateObjects (es/en/pt) + ObjectSelection demo. Returns selector."""
    _EnsurePath()
    from console_helpers import PrintObjectTree, RunCreateObjects, RunSelectionDemo

    target = _FindSketchName(sketch_name)
    if target is None:
        return None

    print("\n========== DAV selection — prueba automática ==========\n")

    for language in ("es", "en", "pt"):
        print(f"--- CreateObjects idioma={language} ---")
        RunCreateObjects(target, Is3D=False, Language=language)
        PrintObjectTree()

    print("--- ObjectSelection (primer objeto) ---")
    selector = RunSelectionDemo()
    if selector is not None:
        print("Para ciclar objetos:")
        print("  selector.SelectOther = True")
        print("(repetí esa línea para avanzar)\n")

    return selector

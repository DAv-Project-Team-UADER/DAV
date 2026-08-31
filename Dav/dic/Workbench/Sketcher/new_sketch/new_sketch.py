# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#
# Este programa se distribuye con la esperanza de que sea útil,
# pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
# MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
# Licencia Pública General GNU para más detalles.
#
# Deberías haber recibido una copia de la Licencia Pública General GNU
# junto con este programa. Si no es así, consulte <http://www.gnu.org/licenses/>.

"""New sketch with a DAV voice-driven plane orientation selector.

Reemplaza al diálogo nativo de FreeCAD (``Sketcher_NewSketch`` →
``SketchOrientationDialog``), que no se puede controlar por voz. Al decir
"nuevo boceto" se abre el selector DAV (``PlaneSelectionInputPrompt``) y el
usuario elige el eje XY/XZ/YZ con "arriba"/"abajo" y confirma con
"okey"/"cancelar". El boceto se crea sobre el plano elegido.
"""

from __future__ import annotations

import sys
from pathlib import Path


def _ensure_input_prompts_on_path() -> None:
    """Make ``InputPrompts`` importable regardless of the current working dir.

    En runtime el motor vive dentro de FreeCAD con GUIFreeCad en sys.path,
    pero los diccionarios pueden cargarse en contextos distintos (tests,
    consola). Se busca ascendiendo hasta toparse con la carpeta InputPrompts.
    """
    if "InputPrompts" in sys.modules or any(
        Path(p).name == "GUIFreeCad" for p in sys.path
    ):
        return
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "InputPrompts").is_dir():
            text = str(parent)
            if text not in sys.path:
                sys.path.insert(0, text)
            return


def _import_plane_prompt():
    _ensure_input_prompts_on_path()
    from InputPrompts.PlaneSelectionInputPrompt import PlaneSelectionInputPrompt

    return PlaneSelectionInputPrompt


# Rotaciones (cuaternión w,x,y,z) idénticas a las que usa el diálogo nativo de
# FreeCAD (SketchOrientationDialog) para cada plano, con MapMode Deactivated.
_PLANE_ROTATIONS = {
    "XY": (1.0, 0.0, 0.0, 0.0),
    "XZ": (1.0, 0.0, 0.0, 1.0),
    "YZ": (1.0, 1.0, 1.0, 1.0),
}


def _new_sketch() -> None:
    """Ask the user (by voice) for the plane and create the sketch on it."""
    import FreeCAD as App

    result = _ask_plane()
    if result is None or result.Cancelled or not result.Value:
        print("[DAV] Nuevo boceto cancelado por el usuario.")
        return

    plane = str(result.Value).upper()
    doc = App.activeDocument()
    if doc is None:
        doc = App.newDocument("SinTítulo")
    if doc is None:
        return

    sketch = doc.addObject("Sketcher::SketchObject", _unique_sketch_name(doc))
    rotation = _PLANE_ROTATIONS.get(plane, _PLANE_ROTATIONS["XY"])
    # App.Rotation(q0, q1, q2, q3) = (w, x, y, z), igual que el nativo.
    sketch.Placement = App.Placement(App.Vector(0, 0, 0), App.Rotation(*rotation))
    sketch.MapMode = "Deactivated"
    doc.recompute()

    # Entrar al modo de edición del boceto recién creado, como hace el nativo.
    try:
        import FreeCADGui as Gui

        Gui.activeDocument().setEdit(sketch.Name)
    except Exception:
        pass

    print(f"[DAV] Nuevo boceto '{sketch.Name}' creado en el plano {plane}.")


def _ask_plane():
    """Show the DAV plane selector and route voice to it."""
    try:
        from InputPrompts.PromptVoiceRouter import PromptVoiceRouter
    except ImportError:
        _ensure_input_prompts_on_path()
        from InputPrompts.PromptVoiceRouter import PromptVoiceRouter

    PlanePrompt = _import_plane_prompt()
    prompt = PlanePrompt()
    PromptVoiceRouter.SetActivePrompt(prompt)
    try:
        return prompt.RequestValue()
    finally:
        PromptVoiceRouter.ClearActivePrompt(prompt)


def _unique_sketch_name(doc) -> str:
    """Return a document-unique name like 'Sketch' or 'Sketch001'."""
    base = "Sketch"
    if doc.getObject(base) is None:
        return base
    index = 1
    while doc.getObject(f"{base}{index:03d}") is not None:
        index += 1
    return f"{base}{index:03d}"


new_sketch = {
    "new": lambda: _new_sketch(),
}

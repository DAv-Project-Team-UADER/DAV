

import FreeCAD as App
import Part
from ..._display import finishFeature
from ..._prompts import askSketch
import FreeCADGui as Gui
from .ayuda import ayuda


def _makeface() -> None:
    """Create a planar face from a closed drawing chosen by voice."""
    doc = App.activeDocument()
    if doc is None:
        print("[part] Error: no active document.")
        return
    source = askSketch(doc, "Crear cara")
    if source is None:
        print("[part] Face cancelled.")
        return
    # Un circulo suelto es una arista cerrada, no un wire: se arma el wire.
    try:
        wires = source.Shape.Wires or [
            Part.Wire(group) for group in Part.sortEdges(source.Shape.Edges)
        ]
    except Exception:
        wires = []
    if not wires:
        print(f"[part] Error: '{source.Name}' has no closed outline.")
        return
    try:
        face = Part.makeFilledFace(wires)
    except Exception as error:
        print(f"[part] Error: could not build a face ({error}).")
        return
    obj = doc.addObject("Part::Feature", "Face")
    obj.Shape = face
    finishFeature(doc, obj, "face", is3D=False, hide=(source,))


part_makeface = {
    'makeface': _makeface,
    'createface': _makeface,
    'upgrade': lambda: Gui.runCommand('Draft_Upgrade', 0),
    'help': ayuda,
}

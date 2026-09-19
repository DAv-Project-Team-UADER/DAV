

import FreeCAD as App
from ..._display import finishFeature
from ..._prompts import askNumber, askSketch
from .ayuda import ayuda


def _extrude() -> None:
    """Extrude a drawing chosen by voice along its normal by a dictated length.

    Elige entre los bocetos y figuras existentes ("avanzar"/"okey") y pide la
    altura; no usa la seleccion del mouse.
    """
    doc = App.activeDocument()
    if doc is None:
        print("[part] Error: no active document.")
        return
    profile = askSketch(doc, "Extruir")
    if profile is None:
        print("[part] Extrusion cancelled.")
        return
    length = askNumber("Extruir", "Decí la altura de extrusión en mm")
    if length is None:
        print("[part] Extrusion cancelled.")
        return
    if length <= 0:
        print(f"[part] Error: the length must be greater than zero (got {length}).")
        return

    extrusion = doc.addObject("Part::Extrusion", "Extrude")
    extrusion.Base = profile
    extrusion.DirMode = "Normal"
    extrusion.LengthFwd = length
    extrusion.Solid = True
    finishFeature(doc, extrusion, "extrusion", hide=(profile,))


part_extrude = {
    'extruir': _extrude,
    'extrude': _extrude,
    'extruir objeto': _extrude,
    'help': ayuda,
}

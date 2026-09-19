

import FreeCAD as App
from ..._display import finishFeature
from ..._prompts import askNumber, askSketch
from .ayuda import ayuda


def _offset2d() -> None:
    """Offset a closed drawing chosen by voice by a dictated distance."""
    doc = App.activeDocument()
    if doc is None:
        print("[part] Error: no active document.")
        return
    source = askSketch(doc, "Contorno")
    if source is None:
        print("[part] Offset cancelled.")
        return
    value = askNumber("Contorno", "Decí la distancia del contorno en mm (negativa hacia adentro)")
    if value is None:
        print("[part] Offset cancelled.")
        return
    if value == 0:
        print("[part] Error: the offset cannot be zero.")
        return

    offset = doc.addObject("Part::Offset2D", "Offset2D")
    offset.Source = source
    offset.Value = value
    finishFeature(doc, offset, "2D offset", is3D=False, hide=(source,))


part_offset2d = {
    'contorno': _offset2d,
    'borde': _offset2d,
    'offset 2d': _offset2d,
    'help': ayuda,
}

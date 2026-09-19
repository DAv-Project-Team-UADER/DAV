

import FreeCAD as App
from ..._display import finishFeature
from ..._prompts import askNumber, askSolid
from .ayuda import ayuda


def _offset() -> None:
    """Thicken (positive) or shrink (negative) a piece chosen by voice."""
    doc = App.activeDocument()
    if doc is None:
        print("[part] Error: no active document.")
        return
    piece = askSolid(doc, "Desfase")
    if piece is None:
        print("[part] Offset cancelled.")
        return
    value = askNumber("Desfase", "Decí cuántos mm ensanchar (negativo para encoger)")
    if value is None:
        print("[part] Offset cancelled.")
        return
    if value == 0:
        print("[part] Error: the offset cannot be zero.")
        return

    offset = doc.addObject("Part::Offset", "Offset3D")
    offset.Source = piece
    offset.Value = value
    finishFeature(doc, offset, "offset", hide=(piece,))


part_offset = {
    'desfase': _offset,
    'offset': _offset,
    'ensanchar': _offset,
    'encoger': _offset,
    'help': ayuda,
}

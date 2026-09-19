

import FreeCAD as App
from ..._display import finishFeature
from ..._prompts import askNumber, askSolid
from .ayuda import ayuda


def _fillet() -> None:
    """Round every edge of a piece chosen by voice with a dictated radius."""
    doc = App.activeDocument()
    if doc is None:
        print("[part] Error: no active document.")
        return
    piece = askSolid(doc, "Redondear")
    if piece is None:
        print("[part] Fillet cancelled.")
        return
    radius = askNumber("Redondear", "Decí el radio del redondeo en mm")
    if radius is None:
        print("[part] Fillet cancelled.")
        return
    if radius <= 0:
        print(f"[part] Error: the radius must be greater than zero (got {radius}).")
        return

    fillet = doc.addObject("Part::Fillet", "Fillet")
    fillet.Base = piece
    fillet.Edges = [(i + 1, radius, radius) for i in range(len(piece.Shape.Edges))]
    finishFeature(doc, fillet, "fillet", hide=(piece,))


part_fillet = {
    'redondear bordes': _fillet,
    'fillet': _fillet,
    'redondear': _fillet,
    'help': ayuda,
}

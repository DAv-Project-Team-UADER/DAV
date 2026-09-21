

import FreeCAD as App
from ..._display import finishFeature
from ..._prompts import askNumber, askSolid
from .ayuda import ayuda


def _chamfer() -> None:
    """Chamfer every edge of a piece chosen by voice with a dictated size."""
    doc = App.activeDocument()
    if doc is None:
        print("[part] Error: no active document.")
        return
    piece = askSolid(doc, "Chaflán")
    if piece is None:
        print("[part] Chamfer cancelled.")
        return
    size = askNumber("Chaflán", "Decí el tamaño del chaflán en mm")
    if size is None:
        print("[part] Chamfer cancelled.")
        return
    if size <= 0:
        print(f"[part] Error: the size must be greater than zero (got {size}).")
        return

    chamfer = doc.addObject("Part::Chamfer", "Chamfer")
    chamfer.Base = piece
    chamfer.Edges = [(i + 1, size, size) for i in range(len(piece.Shape.Edges))]
    finishFeature(doc, chamfer, "chamfer", hide=(piece,))


part_chamfer = {
    'chaflan': _chamfer,
    'chaflán': _chamfer,
    'biselar': _chamfer,
    'help': ayuda,
}

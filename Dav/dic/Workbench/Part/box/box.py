

import FreeCAD as App
from ..._display import finishFeature
from .ayuda import ayuda


def _create_box(x: float, y: float, z: float, length: float, width: float, height: float) -> None:
    """Create a Part box from its starting corner and three dictated dimensions.

    Args:
        x: X of the starting point, in millimetres.
        y: Y of the starting point, in millimetres.
        z: Z of the starting point, in millimetres.
        length: Size along X, in millimetres.
        width: Size along Y, in millimetres.
        height: Size along Z, in millimetres.

    Example::

        _create_box(0, 0, 0, 20, 10, 5)
    """
    if length <= 0 or width <= 0 or height <= 0:
        print("[part] Error: every dimension must be greater than zero.")
        return
    doc = App.activeDocument() or App.newDocument()
    box = doc.addObject("Part::Box", "Box")
    box.Length = length
    box.Width = width
    box.Height = height
    box.Placement = App.Placement(App.Vector(x, y, z), App.Rotation())
    finishFeature(doc, box, "box")


box = {
    'box': _create_box,
    'help': ayuda,
}

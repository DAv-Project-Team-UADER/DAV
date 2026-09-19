

import FreeCAD as App
from ..._display import finishFeature
from .ayuda import ayuda


def _create_box(length: float, width: float, height: float) -> None:
    """Create a Part box from three dictated dimensions.

    Args:
        length: Size along X, in millimetres.
        width: Size along Y, in millimetres.
        height: Size along Z, in millimetres.

    Example::

        _create_box(20, 10, 5)
    """
    if length <= 0 or width <= 0 or height <= 0:
        print("[part] Error: every dimension must be greater than zero.")
        return
    doc = App.activeDocument() or App.newDocument()
    box = doc.addObject("Part::Box", "Box")
    box.Length = length
    box.Width = width
    box.Height = height
    finishFeature(doc, box, "box")


box = {
    'box': _create_box,
    'help': ayuda,
}

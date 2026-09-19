

import FreeCAD as App
from ..._display import finishFeature
from .ayuda import ayuda


def _create_circle(radius: float) -> None:
    """Create a Part circle from a dictated radius.

    Args:
        radius: Circle radius, in millimetres.

    Example::

        _create_circle(8)
    """
    if radius <= 0:
        print("[part] Error: the radius must be greater than zero.")
        return
    doc = App.activeDocument() or App.newDocument()
    circle = doc.addObject("Part::Circle", "Circle")
    circle.Radius = radius
    finishFeature(doc, circle, "circle", is3D=False)


circle = {
    'circle': _create_circle,
    'help':   ayuda,
}

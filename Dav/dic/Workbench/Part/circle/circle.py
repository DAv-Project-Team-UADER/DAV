

import FreeCAD as App
from ..._display import finishFeature
from .ayuda import ayuda


def _create_circle(x: float, y: float, z: float, radius: float) -> None:
    """Create a Part circle from its centre and a dictated radius.

    Args:
        x: X of the centre, in millimetres.
        y: Y of the centre, in millimetres.
        z: Z of the centre, in millimetres.
        radius: Circle radius, in millimetres.

    Example::

        _create_circle(0, 0, 0, 8)
    """
    if radius <= 0:
        print("[part] Error: the radius must be greater than zero.")
        return
    doc = App.activeDocument() or App.newDocument()
    circle = doc.addObject("Part::Circle", "Circle")
    circle.Radius = radius
    circle.Placement = App.Placement(App.Vector(x, y, z), App.Rotation())
    finishFeature(doc, circle, "circle", is3D=False)


circle = {
    'circle': _create_circle,
    'help':   ayuda,
}

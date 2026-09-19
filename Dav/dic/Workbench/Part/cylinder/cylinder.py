

import FreeCAD as App
from ..._display import finishFeature
from .ayuda import ayuda


def _create_cylinder(radius: float, height: float) -> None:
    """Create a Part cylinder from a dictated radius and height.

    Args:
        radius: Base radius, in millimetres.
        height: Cylinder height, in millimetres.

    Example::

        _create_cylinder(5, 20)
    """
    if radius <= 0 or height <= 0:
        print("[part] Error: radius and height must be greater than zero.")
        return
    doc = App.activeDocument() or App.newDocument()
    cylinder = doc.addObject("Part::Cylinder", "Cylinder")
    cylinder.Radius = radius
    cylinder.Height = height
    finishFeature(doc, cylinder, "cylinder")


cylinder = {
    'cylinder':           _create_cylinder,
    'primitive cylinder': _create_cylinder,
    'help':               ayuda,
}



import FreeCAD as App
from ..._display import finishFeature
from .ayuda import ayuda


def _create_cylinder(x: float, y: float, z: float, radius: float, height: float) -> None:
    """Create a Part cylinder from the centre of its base, a radius and a height.

    Args:
        x: X of the base centre, in millimetres.
        y: Y of the base centre, in millimetres.
        z: Z of the base centre, in millimetres.
        radius: Base radius, in millimetres.
        height: Cylinder height, in millimetres.

    Example::

        _create_cylinder(0, 0, 0, 5, 20)
    """
    if radius <= 0 or height <= 0:
        print("[part] Error: radius and height must be greater than zero.")
        return
    doc = App.activeDocument() or App.newDocument()
    cylinder = doc.addObject("Part::Cylinder", "Cylinder")
    cylinder.Radius = radius
    cylinder.Height = height
    cylinder.Placement = App.Placement(App.Vector(x, y, z), App.Rotation())
    finishFeature(doc, cylinder, "cylinder")


cylinder = {
    'cylinder':           _create_cylinder,
    'primitive cylinder': _create_cylinder,
    'help':               ayuda,
}



import FreeCAD as App
from ..._display import finishFeature
from .ayuda import ayuda


def _create_cone(x: float, y: float, z: float, radius1: float, radius2: float, height: float) -> None:
    """Create a Part cone from the centre of its base, two dictated radii and a height.

    Say a second radius of zero for a sharp tip.

    Args:
        x: X of the base centre, in millimetres.
        y: Y of the base centre, in millimetres.
        z: Z of the base centre, in millimetres.
        radius1: Bottom radius, in millimetres.
        radius2: Top radius, in millimetres.
        height: Cone height, in millimetres.

    Example::

        _create_cone(0, 0, 0, 10, 0, 25)
    """
    if radius1 < 0 or radius2 < 0 or height <= 0:
        print("[part] Error: radii cannot be negative and the height must be greater than zero.")
        return
    if radius1 == radius2:
        print("[part] Error: the two radii must differ; use a cylinder instead.")
        return
    doc = App.activeDocument() or App.newDocument()
    cone = doc.addObject("Part::Cone", "Cone")
    cone.Radius1 = radius1
    cone.Radius2 = radius2
    cone.Height = height
    cone.Placement = App.Placement(App.Vector(x, y, z), App.Rotation())
    finishFeature(doc, cone, "cone")


cone = {
    'cone':           _create_cone,
    'primitive cone': _create_cone,
    'help':           ayuda,
}

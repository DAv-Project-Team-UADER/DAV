

import FreeCAD as App
from ..._display import finishFeature
from .ayuda import ayuda


def _create_cube(x: float, y: float, z: float, side: float) -> None:
    """Create a Part cube from its starting corner and a dictated side length.

    Args:
        x: X of the starting point, in millimetres.
        y: Y of the starting point, in millimetres.
        z: Z of the starting point, in millimetres.
        side: Edge length, in millimetres.

    Example::

        _create_cube(0, 0, 0, 15)
    """
    if side <= 0:
        print("[part] Error: the side must be greater than zero.")
        return
    doc = App.activeDocument() or App.newDocument()
    cube = doc.addObject("Part::Box", "Cube")
    cube.Length = side
    cube.Width = side
    cube.Height = side
    cube.Placement = App.Placement(App.Vector(x, y, z), App.Rotation())
    finishFeature(doc, cube, "cube")


cube = {
    'cube': _create_cube,
    'help': ayuda,
}

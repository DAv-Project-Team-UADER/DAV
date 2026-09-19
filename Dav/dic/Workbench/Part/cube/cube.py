

import FreeCAD as App
from ..._display import finishFeature
from .ayuda import ayuda


def _create_cube(side: float) -> None:
    """Create a Part cube from a dictated side length.

    Args:
        side: Edge length, in millimetres.

    Example::

        _create_cube(15)
    """
    if side <= 0:
        print("[part] Error: the side must be greater than zero.")
        return
    doc = App.activeDocument() or App.newDocument()
    cube = doc.addObject("Part::Box", "Cube")
    cube.Length = side
    cube.Width = side
    cube.Height = side
    finishFeature(doc, cube, "cube")


cube = {
    'cube': _create_cube,
    'help': ayuda,
}

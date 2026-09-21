

import FreeCAD as App
from ..._display import finishFeature
from .ayuda import ayuda


def _create_ellipse(x: float, y: float, z: float, major_radius: float, minor_radius: float) -> None:
    """Create a Part ellipse from its centre and a dictated major and minor radius.

    Args:
        x: X of the centre, in millimetres.
        y: Y of the centre, in millimetres.
        z: Z of the centre, in millimetres.
        major_radius: Larger radius, in millimetres.
        minor_radius: Smaller radius, in millimetres. Must not exceed the major one.

    Example::

        _create_ellipse(0, 0, 0, 10, 5)
    """
    if major_radius <= 0 or minor_radius <= 0:
        print("[part] Error: both radii must be greater than zero.")
        return
    if minor_radius > major_radius:
        print("[part] Error: the minor radius cannot exceed the major radius.")
        return
    doc = App.activeDocument() or App.newDocument()
    ellipse = doc.addObject("Part::Ellipse", "Ellipse")
    ellipse.MajorRadius = major_radius
    ellipse.MinorRadius = minor_radius
    ellipse.Placement = App.Placement(App.Vector(x, y, z), App.Rotation())
    finishFeature(doc, ellipse, "ellipse", is3D=False)


ellipse = {
    'ellipse': _create_ellipse,
    'help':    ayuda,
}

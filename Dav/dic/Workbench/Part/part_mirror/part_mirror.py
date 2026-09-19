

import FreeCAD as App
from FreeCAD import Vector
from ..._display import finishFeature
from ..._prompts import askObject, askPlane, isProfile, isSolid
from .ayuda import ayuda

_EMPTY = "[DAV] Error: no hay nada para reflejar. Creá una pieza o un dibujo primero."

# Normal del plano de simetria segun el plano elegido.
_NORMALS = {"XY": Vector(0, 0, 1), "XZ": Vector(0, 1, 0), "YZ": Vector(1, 0, 0)}


def _mirror() -> None:
    """Mirror an object chosen by voice across a plane chosen by voice."""
    doc = App.activeDocument()
    if doc is None:
        print("[part] Error: no active document.")
        return
    source = askObject(
        doc, "Espejo", "Elegí qué reflejar", lambda o: isSolid(o) or isProfile(o), _EMPTY
    )
    if source is None:
        print("[part] Mirror cancelled.")
        return
    plane = askPlane()
    if plane is None:
        print("[part] Mirror cancelled.")
        return

    mirror = doc.addObject("Part::Mirroring", "Mirror")
    mirror.Source = source
    mirror.Normal = _NORMALS.get(plane, _NORMALS["XY"])
    mirror.Base = Vector(0, 0, 0)
    finishFeature(doc, mirror, "mirror", hide=(source,))


part_mirror = {
    'espejo': _mirror,
    'reflejar': _mirror,
    'mirror': _mirror,
    'help': ayuda,
}

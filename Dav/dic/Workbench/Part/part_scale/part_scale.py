

import FreeCAD as App
from ..._display import finishFeature
from ..._prompts import askNumber, askObject, isProfile, isSolid
from .ayuda import ayuda

_EMPTY = "[DAV] Error: no hay nada para escalar. Creá una pieza o un dibujo primero."


def _scale() -> None:
    """Scale an object chosen by voice uniformly by a dictated factor."""
    doc = App.activeDocument()
    if doc is None:
        print("[part] Error: no active document.")
        return
    target = askObject(
        doc, "Escalar", "Elegí qué escalar", lambda o: isSolid(o) or isProfile(o), _EMPTY
    )
    if target is None:
        print("[part] Scale cancelled.")
        return
    factor = askNumber("Escalar", "Decí el factor de escala (2 = doble, 0.5 = mitad)")
    if factor is None:
        print("[part] Scale cancelled.")
        return
    if factor <= 0:
        print(f"[part] Error: the factor must be greater than zero (got {factor}).")
        return

    scale = doc.addObject("Part::Scale", "Scale")
    scale.Base = target
    scale.Uniform = True
    scale.UniformScale = factor
    finishFeature(doc, scale, "scale", hide=(target,))


part_scale = {
    'escalar': _scale,
    'agrandar': _scale,
    'reducir': _scale,
    'scale': _scale,
    'help': ayuda,
}

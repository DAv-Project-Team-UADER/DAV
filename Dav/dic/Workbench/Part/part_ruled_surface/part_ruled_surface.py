

import FreeCAD as App
from ..._display import finishFeature
from ..._prompts import askObject, isProfile
from .ayuda import ayuda

_EMPTY = "[DAV] Error: no hay curvas para unir. Dibujá dos perfiles."


def _ruled_surface() -> None:
    """Create a ruled surface between two drawings chosen by voice."""
    doc = App.activeDocument()
    if doc is None:
        print("[part] Error: no active document.")
        return
    first = askObject(doc, "Superficie reglada", "Elegí la primera curva", isProfile, _EMPTY)
    if first is None:
        print("[part] Ruled surface cancelled.")
        return
    second = askObject(
        doc, "Superficie reglada", "Elegí la segunda curva",
        lambda o: isProfile(o) and o is not first, _EMPTY,
    )
    if second is None:
        print("[part] Ruled surface cancelled.")
        return

    surface = doc.addObject("Part::RuledSurface", "RuledSurface")
    surface.Curve1 = (first, ["Edge1"])
    surface.Curve2 = (second, ["Edge1"])
    finishFeature(doc, surface, "ruled surface", is3D=False, hide=(first, second))


part_ruled_surface = {
    'superficie reglada': _ruled_surface,
    'unir curvas': _ruled_surface,
    'ruled surface': _ruled_surface,
    'help': ayuda,
}

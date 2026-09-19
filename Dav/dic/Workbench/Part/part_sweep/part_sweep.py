

import FreeCAD as App
from ..._display import finishFeature
from ..._prompts import askObject, isProfile
from .ayuda import ayuda

_EMPTY = "[DAV] Error: no hay dibujos para barrer. Dibujá un perfil y un camino."


def _sweep() -> None:
    """Sweep a profile chosen by voice along a path chosen by voice."""
    doc = App.activeDocument()
    if doc is None:
        print("[part] Error: no active document.")
        return
    profile = askObject(doc, "Barrido", "Elegí el perfil", isProfile, _EMPTY)
    if profile is None:
        print("[part] Sweep cancelled.")
        return
    path = askObject(
        doc, "Barrido", "Elegí el camino", lambda o: isProfile(o) and o is not profile, _EMPTY
    )
    if path is None:
        print("[part] Sweep cancelled.")
        return

    sweep = doc.addObject("Part::Sweep", "Sweep")
    sweep.Sections = [profile]
    sweep.Spine = (path, ["Edge1"])
    sweep.Solid = True
    sweep.Frenet = False
    finishFeature(doc, sweep, "sweep", hide=(profile, path))


part_sweep = {
    'barrer perfil': _sweep,
    'sweep': _sweep,
    'barrido': _sweep,
    'help': ayuda,
}



import FreeCAD as App
from ..._display import finishFeature
from ..._prompts import askObject, isProfile
from .ayuda import ayuda

_EMPTY = "[DAV] Error: no hay dibujos para unir. Dibujá al menos dos perfiles."


def _loft() -> None:
    """Loft between two drawings chosen by voice (first and last profile)."""
    doc = App.activeDocument()
    if doc is None:
        print("[part] Error: no active document.")
        return
    first = askObject(doc, "Loft", "Elegí el primer perfil", isProfile, _EMPTY)
    if first is None:
        print("[part] Loft cancelled.")
        return
    second = askObject(
        doc, "Loft", "Elegí el segundo perfil", lambda o: isProfile(o) and o is not first, _EMPTY
    )
    if second is None:
        print("[part] Loft cancelled.")
        return

    loft = doc.addObject("Part::Loft", "Loft")
    loft.Sections = [first, second]
    loft.Solid = True
    loft.Ruled = False
    finishFeature(doc, loft, "loft", hide=(first, second))


part_loft = {
    'hacer loft': _loft,
    'loft': _loft,
    'unir perfiles': _loft,
    'help': ayuda,
}

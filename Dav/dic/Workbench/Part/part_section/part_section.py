

import FreeCAD as App
from ..._display import finishFeature
from ..._prompts import askObject, isSolid
from .ayuda import ayuda

_EMPTY = "[DAV] Error: hacen falta dos piezas sólidas para obtener su sección."


def _section() -> None:
    """Create the section curve between two solid pieces chosen by voice."""
    doc = App.activeDocument()
    if doc is None:
        print("[part] Error: no active document.")
        return
    base = askObject(doc, "Sección", "Elegí la primera pieza", isSolid, _EMPTY)
    if base is None:
        print("[part] Section cancelled.")
        return
    tool = askObject(
        doc, "Sección", "Elegí la segunda pieza", lambda o: isSolid(o) and o is not base, _EMPTY
    )
    if tool is None:
        print("[part] Section cancelled.")
        return

    section = doc.addObject("Part::Section", "Section")
    section.Base = base
    section.Tool = tool
    finishFeature(doc, section, "section", is3D=False, hide=(base, tool))


part_section = {
    'intersección': _section,
    'obtener sección': _section,
    'section': _section,
    'help': ayuda,
}

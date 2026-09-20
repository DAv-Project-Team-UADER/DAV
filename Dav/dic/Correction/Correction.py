# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#
# Este programa se distribuye con la esperanza de que sea útil,
# pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
# MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
# Licencia Pública General GNU para más detalles.
#
# Deberías haber recibido una copia de la Licencia Pública General GNU
# junto con este programa. Si no es así, consulte <http://www.gnu.org/licenses/>.

"""Fix mistakes by voice: undo, delete the last object, delete a chosen one, clean broken ones.

Estos comandos viven en el diccionario raíz (ver TraduceTo*.py de ``dic/``),
así que se pueden decir desde cualquier contexto sin navegar hasta Explorer.
Borrar siempre pide confirmación por voz: no se puede deshacer desde acá.
"""

import FreeCAD as App
import FreeCADGui as Gui

from .ayuda import ayuda

# Los objetos del origen de un Body/Part se crean solos y no se borran por separado.
_ORIGIN_TYPES = ("App::Origin", "App::Line", "App::Plane", "App::Point")


def undo() -> None:
    """Undo the last change made in the active document."""
    Gui.runCommand("Std_Undo", 0)


def redo() -> None:
    """Redo the last undone change."""
    Gui.runCommand("Std_Redo", 0)


def _isDeletable(obj) -> bool:
    """True for objects the user can delete on their own (not origin planes or axes)."""
    return obj.TypeId not in _ORIGIN_TYPES


def _dependents(obj) -> list:
    """Return the objects that use ``obj`` (other than the group that holds it)."""
    holder = None
    try:
        holder = obj.getParentGeoFeatureGroup()
    except Exception:
        pass
    return [
        other
        for other in obj.InList
        if other is not holder and not (hasattr(other, "Group") and obj in other.Group)
    ]


def _remove(doc, obj) -> None:
    """Remove obj (and, for a body, everything inside it) from the document."""
    if obj.isDerivedFrom("PartDesign::Body"):
        obj.removeObjectsFromDocument()
        doc.removeObject(obj.Name)
        return
    holder = None
    try:
        holder = obj.getParentGeoFeatureGroup()
    except Exception:
        pass
    if holder is not None and hasattr(holder, "removeObject"):
        holder.removeObject(obj)
    doc.removeObject(obj.Name)


def _confirmAndDelete(doc, objects: list, question: str) -> bool:
    """Ask for confirmation, then delete ``objects`` (newest first).

    Returns:
        True when something was deleted.
    """
    from Workbench._prompts import askYesNo

    if not askYesNo("Borrar", question):
        print("[DAV] Borrado cancelado.")
        return False
    deleted = 0
    for obj in reversed(objects):
        # un cuerpo borrado ya se llevó consigo lo que tenía adentro
        if doc.getObject(obj.Name) is None:
            continue
        try:
            _remove(doc, obj)
            deleted += 1
        except Exception as error:
            print(f"[DAV] No se pudo borrar '{getattr(obj, 'Name', obj)}': {error}")
    doc.recompute()
    print(f"[DAV] Se borraron {deleted} objeto/s.")
    return deleted > 0


def _refuseIfInUse(obj) -> bool:
    """Print a message and return True when other objects still depend on ``obj``."""
    users = _dependents(obj)
    if not users:
        return False
    names = ", ".join(user.Name for user in users)
    print(f"[DAV] No se puede borrar '{obj.Name}': lo usan {names}. Borrá esos primero.")
    return True


def deleteLast() -> None:
    """Delete the object created last, after asking for confirmation."""
    doc = App.activeDocument()
    if doc is None:
        print("[DAV] Error: no hay documento activo.")
        return
    candidates = [obj for obj in doc.Objects if _isDeletable(obj)]
    if not candidates:
        print("[DAV] No hay objetos para borrar.")
        return
    last = candidates[-1]
    if _refuseIfInUse(last):
        return
    _confirmAndDelete(doc, [last], f"¿Borrar '{last.Name}'? Decí sí o no")


def deleteObject() -> None:
    """Choose any object from the list (broken ones included) and delete it."""
    from Workbench._prompts import askObject

    doc = App.activeDocument()
    if doc is None:
        print("[DAV] Error: no hay documento activo.")
        return
    obj = askObject(
        doc, "Borrar objeto", "Elegí el objeto a borrar", _isDeletable,
        "[DAV] No hay objetos para borrar.",
    )
    if obj is None:
        return
    if _refuseIfInUse(obj):
        return
    _confirmAndDelete(doc, [obj], f"¿Borrar '{obj.Name}'? Decí sí o no")


def deleteBroken() -> None:
    """Delete every object that failed to recompute, after asking for confirmation.

    Un objeto roto (por ejemplo un agujero que no se pudo crear) deja inservible
    el cuerpo que lo contiene: acá se limpian todos juntos.
    """
    doc = App.activeDocument()
    if doc is None:
        print("[DAV] Error: no hay documento activo.")
        return
    doc.recompute()
    # el cuerpo en sí no se borra: con quitarle la operación rota vuelve a servir
    broken = [
        obj for obj in doc.Objects
        if _isDeletable(obj) and not obj.isValid() and not obj.isDerivedFrom("PartDesign::Body")
    ]
    if not broken:
        print("[DAV] No hay objetos rotos.")
        return
    names = ", ".join(obj.Name for obj in broken)
    _confirmAndDelete(doc, broken, f"¿Borrar {len(broken)} objeto/s roto/s ({names})? Decí sí o no")


correction = {
    "undo": undo,
    "redo": redo,
    "deletelast": deleteLast,
    "deleteobject": deleteObject,
    "deletebroken": deleteBroken,
    "help": ayuda,
}

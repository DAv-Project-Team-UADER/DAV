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

"""New PartDesign sketch with the same DAV voice plane selector as Sketcher.

Reemplaza al diálogo nativo de ``PartDesign_NewSketch``, que no se controla
por voz. Reutiliza el selector de plano del Sketcher (arriba/abajo/okey/
cancelar) y crea el boceto dentro del Body activo, adjunto al plano base
elegido del Origin del Body.
"""

from __future__ import annotations

from ..._display import enterSketcherContext
from ...Sketcher.new_sketch._faces import attachSketchToFace, listPlanarFaces
from ...Sketcher.new_sketch.new_sketch import _ask_plane, _unique_sketch_name

# Rol de cada plano en el Origin de un Body de PartDesign.
_PLANE_ROLES = {
    "XY": "XY_Plane",
    "XZ": "XZ_Plane",
    "YZ": "YZ_Plane",
}


def _activeBody(doc):
    """Return the active Body, creating and activating one if none exists.

    Args:
        doc: Active FreeCAD document.

    Returns:
        The active ``PartDesign::Body``.
    """
    import FreeCADGui as Gui

    view = Gui.activeView()
    body = view.getActiveObject("pdbody") if view is not None else None
    if body is not None:
        return body

    body = doc.addObject("PartDesign::Body", "Body")
    if view is not None:
        view.setActiveObject("pdbody", body)
    return body


def _originPlane(body, plane: str):
    """Return the Origin plane object of ``body`` for 'XY', 'XZ' or 'YZ'."""
    role = _PLANE_ROLES.get(plane, _PLANE_ROLES["XY"])
    for feature in body.Origin.OriginFeatures:
        if feature.Role == role:
            return feature
    return None


def _new_sketch_partdesign() -> None:
    """Ask the user (by voice) for a plane or a face and create the sketch in the Body."""
    import FreeCAD as App

    faces = listPlanarFaces(App.activeDocument())
    result = _ask_plane(faces)
    if result is None or result.Cancelled or not result.Value:
        print("[DAV] Nuevo boceto cancelado por el usuario.")
        return

    choice = str(result.Value)
    doc = App.activeDocument()
    if doc is None:
        doc = App.newDocument("SinTítulo")
    if doc is None:
        return

    if choice in faces:
        option = faces[choice]
        # el boceto va en el Body dueño de la cara, no en uno nuevo
        body = option["body"] or _activeBody(doc)
        sketch = body.newObject("Sketcher::SketchObject", _unique_sketch_name(doc))
        attachSketchToFace(sketch, option)
        where = f"la {option['label'].lower()}"
    else:
        plane = choice.upper()
        body = _activeBody(doc)
        origin_plane = _originPlane(body, plane)
        if origin_plane is None:
            print(f"[DAV] No se encontró el plano {plane} en el Body '{body.Name}'.")
            return

        sketch = body.newObject("Sketcher::SketchObject", _unique_sketch_name(doc))
        # FreeCAD 0.21 usa "Support"; 1.x lo renombró a "AttachmentSupport".
        support = "AttachmentSupport" if hasattr(sketch, "AttachmentSupport") else "Support"
        setattr(sketch, support, [(origin_plane, "")])
        sketch.MapMode = "FlatFace"
        where = f"el plano {plane}"
    doc.recompute()

    # Entrar al modo de edición del boceto recién creado, como hace el nativo.
    try:
        import FreeCADGui as Gui

        Gui.activeDocument().setEdit(sketch.Name)
    except Exception:
        pass

    print(f"[DAV] Nuevo boceto '{sketch.Name}' creado en {where} del Body '{body.Name}'.")
    enterSketcherContext()

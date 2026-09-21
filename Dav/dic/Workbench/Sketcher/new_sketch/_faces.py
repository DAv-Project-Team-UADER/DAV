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

"""Planar faces of the solid being edited, offered as sketch supports.

El selector de "nuevo boceto" lista primero los planos base (XY, XZ, YZ) y, a
continuación, las caras planas del sólido en el que se está trabajando, para
poder dibujar (por ejemplo, círculos para agujerear) directamente sobre ellas.
"""

from __future__ import annotations

import FreeCAD as App
import Part

# tope de caras que se ofrecen: recorrerlas por voz con arriba/abajo se vuelve
# inmanejable cuando el sólido tiene decenas (p. ej. el fondo de cada agujero)
_MAX_FACES = 12

# nombre hablado según hacia dónde mira la normal de la cara, con las mismas
# convenciones de vistas de FreeCAD (frontal = mira hacia -Y)
_AXIS_NAMES = {
    (0, 0, 1): "superior",
    (0, 0, -1): "inferior",
    (0, -1, 0): "frontal",
    (0, 1, 0): "trasera",
    (1, 0, 0): "derecha",
    (-1, 0, 0): "izquierda",
}


def _resolveSolid(obj):
    """Return ``(support, body)`` whose shape holds the faces for ``obj``.

    Args:
        obj: A Body, a feature inside a Body, or a plain Part solid.

    Returns:
        The support object to attach to (a Body's Tip, or the solid itself) and
        the owning Body (None for a solid outside any Body), or ``(None, None)``.
    """
    if obj is None:
        return None, None
    body = obj if obj.isDerivedFrom("PartDesign::Body") else None
    if body is None and hasattr(obj, "getParentGeoFeatureGroup"):
        parent = obj.getParentGeoFeatureGroup()
        if parent is not None and parent.isDerivedFrom("PartDesign::Body"):
            body = parent
    if body is not None:
        return (body.Tip, body) if body.Tip is not None else (None, None)
    shape = getattr(obj, "Shape", None)
    if shape is not None and shape.Solids:
        return obj, None
    return None, None


def findSolid(doc):
    """Pick the solid to work on: selection, active Body or newest solid.

    Args:
        doc: Active FreeCAD document.

    Returns:
        ``(support, body)``: the object whose shape holds the solid and its
        owning Body (None for a solid outside any Body); ``(None, None)`` when
        the document has no solid.
    """
    candidates = []
    try:
        import FreeCADGui as Gui

        candidates.extend(Gui.Selection.getSelection())
        view = Gui.activeView()
        active = view.getActiveObject("pdbody") if view is not None else None
        if active is not None:
            candidates.append(active)
    except Exception:
        pass
    # sin selección ni Body activo: el último cuerpo, o el último sólido suelto
    bodies = [o for o in doc.Objects if o.isDerivedFrom("PartDesign::Body")]
    if bodies:
        candidates.append(bodies[-1])
    candidates.extend(
        o for o in reversed(doc.Objects)
        if o.isDerivedFrom("Part::Feature") and not o.isDerivedFrom("Sketcher::SketchObject")
    )
    for obj in candidates:
        support, body = _resolveSolid(obj)
        if support is not None:
            return support, body
    return None, None


def listPlanarFaces(doc) -> dict:
    """List the planar faces of the solid being edited, largest first.

    Args:
        doc: Active FreeCAD document (may be None).

    Returns:
        Ordered dict keyed by face name (``"Face3"``). Each value holds
        ``label`` (spoken name), ``support``, ``subname``, ``center`` and
        ``body``. Empty when there is no solid to sketch on.

    Example::

        faces = listPlanarFaces(App.activeDocument())
    """
    if doc is None:
        return {}
    support, body = findSolid(doc)
    if support is None:
        return {}

    planar = []
    for index, face in enumerate(support.Shape.Faces, 1):
        if not isinstance(face.Surface, Part.Plane):
            continue
        u, v = face.Surface.parameter(face.CenterOfMass)
        normal = face.normalAt(u, v)
        key = tuple(int(round(c)) for c in (normal.x, normal.y, normal.z))
        planar.append((face.Area, index, _AXIS_NAMES.get(key, "inclinada"), face.CenterOfMass))
    planar.sort(key=lambda item: -item[0])

    faces = {}
    seen = {}
    for _area, index, name, center in planar[:_MAX_FACES]:
        seen[name] = seen.get(name, 0) + 1
        suffix = f" {seen[name]}" if seen[name] > 1 else ""
        faces[f"Face{index}"] = {
            "label": f"Cara {name}{suffix}",
            "support": support,
            "subname": f"Face{index}",
            "center": center,
            "body": body,
        }
    return faces


def attachSketchToFace(sketch, option: dict) -> None:
    """Map ``sketch`` flat onto a face returned by :func:`listPlanarFaces`.

    The sketch origin is moved to the centre of the face, so coordinates
    dictated by voice are measured from the middle of it.

    Args:
        sketch: The ``Sketcher::SketchObject`` to attach.
        option: One value of the dict returned by :func:`listPlanarFaces`.
    """
    # FreeCAD 0.21 usa "Support"; 1.x lo renombró a "AttachmentSupport".
    attribute = "AttachmentSupport" if hasattr(sketch, "AttachmentSupport") else "Support"
    setattr(sketch, attribute, [(option["support"], option["subname"])])
    sketch.MapMode = "FlatFace"
    sketch.Document.recompute()

    # FreeCAD pone el origen donde le conviene; se lo lleva al centro de la cara
    local = sketch.Placement.inverse().multVec(option["center"])
    sketch.AttachmentOffset = App.Placement(App.Vector(local.x, local.y, 0), App.Rotation())
    sketch.Document.recompute()

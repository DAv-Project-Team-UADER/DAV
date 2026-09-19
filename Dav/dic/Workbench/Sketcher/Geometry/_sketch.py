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

"""Helpers to draw DAV geometry inside a Sketcher sketch.

Los comandos de geometria creaban objetos ``Part::Feature`` sueltos; si el
usuario estaba editando un boceto (por ejemplo el de PartDesign) el dibujo
quedaba afuera y el boceto vacio no se podia extruir.
"""

from __future__ import annotations

import Part


def editedSketch(doc):
    """Return the sketch being edited (or the active one), or None.

    Args:
        doc: Active FreeCAD document.

    Returns:
        A ``Sketcher::SketchObject`` or None when no sketch is in use.
    """
    try:
        import FreeCADGui as Gui

        view_object = Gui.ActiveDocument.getInEdit()
        obj = getattr(view_object, "Object", None)
        if obj is not None and obj.TypeId == "Sketcher::SketchObject":
            return obj
    except Exception:
        pass
    active = getattr(doc, "ActiveObject", None)
    if active is not None and getattr(active, "TypeId", "") == "Sketcher::SketchObject":
        return active
    return None


def _geometryFromEdge(edge):
    """Convert a Part edge into geometry a sketch accepts, or None."""
    curve = edge.Curve
    first, last = edge.FirstParameter, edge.LastParameter
    closed = edge.isClosed()

    if isinstance(curve, Part.Line):
        return Part.LineSegment(edge.Vertexes[0].Point, edge.Vertexes[-1].Point)
    if isinstance(curve, Part.Circle):
        return curve if closed else Part.ArcOfCircle(curve, first, last)
    if isinstance(curve, Part.Ellipse):
        return curve if closed else Part.ArcOfEllipse(curve, first, last)
    if isinstance(curve, Part.Hyperbola):
        return Part.ArcOfHyperbola(curve, first, last)
    if isinstance(curve, Part.Parabola):
        return Part.ArcOfParabola(curve, first, last)
    if isinstance(curve, Part.BSplineCurve):
        spline = curve.copy()
        spline.segment(first, last)
        return spline
    try:
        return edge.Curve.toBSpline(first, last)
    except Exception:
        return None


def shapeToSketchGeometry(shape) -> list:
    """Return the sketch geometry for every convertible edge of shape."""
    geometry = []
    for edge in shape.Edges:
        item = _geometryFromEdge(edge)
        if item is None:
            print(f"[DAV] Arista no convertible a boceto: {type(edge.Curve).__name__}")
            continue
        geometry.append(item)
    return geometry


def addToEditedSketch(doc, shape) -> bool:
    """Draw shape into the sketch being edited.

    Args:
        doc: Active FreeCAD document.
        shape: Part shape whose edges are added.

    Returns:
        True when a sketch took the shape; False means the caller should
        create a loose object as before.
    """
    sketch = editedSketch(doc)
    if sketch is None:
        return False
    geometry = shapeToSketchGeometry(shape)
    if not geometry:
        return False
    sketch.addGeometry(geometry, False)
    doc.recompute()
    print(f"[DAV] Dibujado en el boceto '{sketch.Name}'.")
    return True

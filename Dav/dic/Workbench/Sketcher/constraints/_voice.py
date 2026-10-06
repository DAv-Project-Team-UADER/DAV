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

"""Geometric sketch constraints driven by voice: sketch and elements are chosen from lists.

Las restricciones geométricas dependían de haber seleccionado la geometría
con el mouse. Acá el boceto se elige de una lista y los elementos por número
(el orden de dibujo, desde 1). Las cotas (dimensión, radio, ángulo...) NO se
tocan: siguen como estaban en ``constraints.py``.
"""

import Sketcher

from ..._prompts import askNumber
from .._elements import askElement, askPointPosition, askSketchObject

# Restricciones con valor (cotas): son las que se pueden pasar a «referencia».
_DIMENSIONAL = ("Distance", "DistanceX", "DistanceY", "Radius", "Diameter", "Angle", "Weight")
_CURVES_WITH_CENTRE = ("Part::GeomCircle", "Part::GeomEllipse", "Part::GeomArcOfEllipse")


def _add(doc, sketch, constraint, done: str, several=None) -> None:
    """Add a constraint (or the list ``several`` at once), recompute and report.

    A refused constraint is printed, not raised.
    """
    try:
        sketch.addConstraint(several if several is not None else constraint)
        doc.recompute()
    except Exception as error:
        print(f"[DAV] Error: no se pudo agregar la restricción en '{sketch.Name}': {error}")
        return
    print(f"[DAV] {done} en '{sketch.Name}'.")


def _single(title: str, kind: str, done: str) -> None:
    """Add a constraint that needs one element (horizontal, vertical, block)."""
    doc, sketch = askSketchObject(title)
    if sketch is None:
        return
    geo = askElement(sketch, title)
    if geo is None:
        return
    _add(doc, sketch, Sketcher.Constraint(kind, geo), done)


def _pair(title: str, kind: str, done: str) -> None:
    """Add a constraint between two elements (parallel, perpendicular, equal, tangent)."""
    doc, sketch = askSketchObject(title)
    if sketch is None:
        return
    first = askElement(sketch, title, "Decí el número del primer elemento")
    if first is None:
        return
    second = askElement(sketch, title, "Decí el número del segundo elemento")
    if second is None:
        return
    if first == second:
        print("[DAV] Error: hay que elegir dos elementos distintos.")
        return
    _add(doc, sketch, Sketcher.Constraint(kind, first, second), done)


def make_horizontal() -> None:
    """Force a line to be horizontal."""
    _single("Horizontal", "Horizontal", "Línea horizontal")


def make_vertical() -> None:
    """Force a line to be vertical."""
    _single("Vertical", "Vertical", "Línea vertical")


def make_block() -> None:
    """Block an element so it cannot move."""
    _single("Bloquear", "Block", "Elemento bloqueado")


def make_parallel() -> None:
    """Make two lines parallel."""
    _pair("Paralelo", "Parallel", "Líneas paralelas")


def make_perpendicular() -> None:
    """Make two lines perpendicular."""
    _pair("Perpendicular", "Perpendicular", "Líneas perpendiculares")


def make_equal() -> None:
    """Make two elements the same size (equal length or radius)."""
    _pair("Igual", "Equal", "Elementos iguales")


def make_tangent() -> None:
    """Make two elements tangent to each other."""
    _pair("Tangente", "Tangent", "Elementos tangentes")


def make_coincident() -> None:
    """Join a point of one element with a point of another."""
    doc, sketch = askSketchObject("Coincidente")
    if sketch is None:
        return
    first = askElement(sketch, "Coincidente", "Decí el número del primer elemento")
    if first is None:
        return
    firstPoint = askPointPosition("Coincidente", "Elegí el punto del primer elemento")
    if firstPoint is None:
        return
    second = askElement(sketch, "Coincidente", "Decí el número del segundo elemento")
    if second is None:
        return
    secondPoint = askPointPosition("Coincidente", "Elegí el punto del segundo elemento")
    if secondPoint is None:
        return
    _add(
        doc, sketch, Sketcher.Constraint("Coincident", first, firstPoint, second, secondPoint),
        "Puntos unidos",
    )


def make_point_on_object() -> None:
    """Force a point of one element to lie on another element."""
    doc, sketch = askSketchObject("Punto sobre objeto")
    if sketch is None:
        return
    first = askElement(sketch, "Punto sobre objeto", "Decí el número del elemento que tiene el punto")
    if first is None:
        return
    point = askPointPosition("Punto sobre objeto", "Elegí el punto")
    if point is None:
        return
    second = askElement(sketch, "Punto sobre objeto", "Decí el número del elemento sobre el que va")
    if second is None:
        return
    _add(doc, sketch, Sketcher.Constraint("PointOnObject", first, point, second), "Punto sobre el objeto")


def _askPointOf(sketch, geo: int, title: str, message: str):
    """Ask which point of element ``geo``; only the points it really has are offered.

    Un círculo o una elipse solo tienen centro y un punto solo tiene un punto: ahí no se pregunta.
    """
    typeId = sketch.Geometry[geo].TypeId
    if typeId == "Part::GeomPoint":
        return 1
    if typeId in _CURVES_WITH_CENTRE:
        return 3
    return askPointPosition(title, message, withCenter=typeId == "Part::GeomArcOfCircle")


def make_lock() -> None:
    """Fix a point where it is now (distances to the origin), so it cannot move."""
    title = "Fijar posición"
    doc, sketch = askSketchObject(title)
    if sketch is None:
        return
    geo = askElement(sketch, title, "Decí el número del elemento")
    if geo is None:
        return
    pos = _askPointOf(sketch, geo, title, "Elegí el punto que se fija")
    if pos is None:
        return
    point = sketch.getPoint(geo, pos)
    _add(
        doc, sketch, None, f"Punto fijo en ({point.x:g}, {point.y:g})",
        [
            Sketcher.Constraint("DistanceX", -1, 1, geo, pos, point.x),
            Sketcher.Constraint("DistanceY", -1, 1, geo, pos, point.y),
        ],
    )


def make_coincident_unified() -> None:
    """Join two points. En voz es lo mismo que «coincidente»: se eligen los dos puntos."""
    make_coincident()


def make_horizontal_or_vertical() -> None:
    """Make a line horizontal or vertical, whichever is closer to how it is drawn."""
    title = "Horizontal o vertical"
    doc, sketch = askSketchObject(title)
    if sketch is None:
        return
    geo = askElement(sketch, title, "Decí el número de la línea")
    if geo is None:
        return
    if sketch.Geometry[geo].TypeId != "Part::GeomLineSegment":
        print("[DAV] Error: este comando es para líneas; el elemento elegido no lo es.")
        return
    start, end = sketch.getPoint(geo, 1), sketch.getPoint(geo, 2)
    horizontal = abs(end.x - start.x) >= abs(end.y - start.y)
    _add(
        doc, sketch, Sketcher.Constraint("Horizontal" if horizontal else "Vertical", geo),
        "Línea horizontal" if horizontal else "Línea vertical",
    )


def _askConstraint(sketch, title: str, onlyDimensions: bool):
    """Ask for a constraint by its number; returns its 0-based index or None.

    La numeración es la del panel de restricciones de FreeCAD (desde 1). Se nombran solo las
    que sirven: las cotas para «referencia», todas para «activar/desactivar».
    """
    rows = []
    for index, constraint in enumerate(sketch.Constraints):
        if onlyDimensions and constraint.Type not in _DIMENSIONAL:
            continue
        value = f" {constraint.Value:g}" if constraint.Type in _DIMENSIONAL else ""
        rows.append((index, f"{index + 1} {constraint.Type}{value}"))
    if not rows:
        print("[DAV] Error: el boceto no tiene restricciones" + (" con medida." if onlyDimensions else "."))
        return None
    number = askNumber(title, f"Decí el número de la restricción ({', '.join(text for _i, text in rows)})")
    if number is None:
        print(f"[DAV] {title} cancelado.")
        return None
    chosen = int(number) - 1
    if chosen not in [index for index, _text in rows]:
        print(f"[DAV] Error: la restricción {int(number)} no está entre las ofrecidas.")
        return None
    return chosen


def toggle_driving() -> None:
    """Switch a dimension between driving (it moves the drawing) and reference (it only measures)."""
    title = "Conductora o referencia"
    doc, sketch = askSketchObject(title)
    if sketch is None:
        return
    index = _askConstraint(sketch, title, onlyDimensions=True)
    if index is None:
        return
    try:
        sketch.toggleDriving(index)
        doc.recompute()
    except Exception as error:
        print(f"[DAV] Error: no se pudo cambiar la restricción {index + 1}: {error}")
        return
    state = "conductora" if sketch.getDriving(index) else "de referencia"
    print(f"[DAV] La restricción {index + 1} de '{sketch.Name}' ahora es {state}.")


def toggle_active() -> None:
    """Turn a constraint off (it stops applying) or back on."""
    title = "Activar o desactivar"
    doc, sketch = askSketchObject(title)
    if sketch is None:
        return
    index = _askConstraint(sketch, title, onlyDimensions=False)
    if index is None:
        return
    try:
        sketch.toggleActive(index)
        doc.recompute()
    except Exception as error:
        print(f"[DAV] Error: no se pudo cambiar la restricción {index + 1}: {error}")
        return
    state = "activa" if sketch.getActive(index) else "desactivada"
    print(f"[DAV] La restricción {index + 1} de '{sketch.Name}' ahora está {state}.")


def make_symmetric() -> None:
    """Make two points symmetric about a line."""
    doc, sketch = askSketchObject("Simétrico")
    if sketch is None:
        return
    first = askElement(sketch, "Simétrico", "Decí el número del primer elemento")
    if first is None:
        return
    firstPoint = askPointPosition("Simétrico", "Elegí el punto del primer elemento")
    if firstPoint is None:
        return
    second = askElement(sketch, "Simétrico", "Decí el número del segundo elemento")
    if second is None:
        return
    secondPoint = askPointPosition("Simétrico", "Elegí el punto del segundo elemento")
    if secondPoint is None:
        return
    axis = askElement(sketch, "Simétrico", "Decí el número de la línea de simetría")
    if axis is None:
        return
    _add(
        doc, sketch,
        Sketcher.Constraint("Symmetric", first, firstPoint, second, secondPoint, axis),
        "Puntos simétricos",
    )

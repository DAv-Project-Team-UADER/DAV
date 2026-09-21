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

from .._elements import askElement, askPointPosition, askSketchObject


def _add(doc, sketch, constraint, done: str) -> None:
    """Add a constraint, recompute and report; a refused constraint is printed, not raised."""
    try:
        sketch.addConstraint(constraint)
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

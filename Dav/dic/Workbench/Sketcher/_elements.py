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

"""Voice prompts to pick a sketch, one of its elements and a point of it.

Las ediciones y restricciones nativas del Sketcher esperan que el usuario
haga clic sobre la geometría. Acá se elige el boceto de una lista y el
elemento por número (el orden en que se dibujaron, desde 1); el mensaje del
pedido lista los elementos con su tipo para saber cuál es cuál.
"""

import FreeCAD as App

from .._prompts import askChoice, askNumber, askObject, isSketch

_TYPE_NAMES = {
    "Part::GeomLineSegment": "línea",
    "Part::GeomCircle": "círculo",
    "Part::GeomArcOfCircle": "arco",
    "Part::GeomPoint": "punto",
    "Part::GeomEllipse": "elipse",
    "Part::GeomArcOfEllipse": "arco de elipse",
    "Part::GeomBSplineCurve": "curva",
}


def describeElements(sketch) -> str:
    """Return the sketch elements as ``1 línea, 2 círculo...`` (numbering from 1)."""
    return ", ".join(
        f"{index} {_TYPE_NAMES.get(geo.TypeId, 'curva')}"
        for index, geo in enumerate(sketch.Geometry, start=1)
    )


def askSketchObject(title: str):
    """Ask which sketch to work on.

    Returns:
        ``(doc, sketch)``, or ``(None, None)`` when cancelled or there are none.
    """
    doc = App.activeDocument()
    if doc is None:
        print("[DAV] Error: no hay documento activo.")
        return None, None
    sketch = askObject(
        doc,
        title,
        "Elegí el boceto",
        isSketch,
        "[DAV] Error: no hay ningún boceto con dibujo. Dibujá algo en un boceto primero.",
    )
    if sketch is None:
        print(f"[DAV] {title} cancelado.")
        return None, None
    return doc, sketch


def askElement(sketch, title: str, message: str = "Decí el número del elemento"):
    """Ask for one element of the sketch by its number.

    Args:
        sketch: The sketch that holds the elements.
        title: Dialog title.
        message: What the element is for; the element list is appended.

    Returns:
        The geometry index (0-based, as Sketcher uses it), or None when cancelled
        or out of range.
    """
    number = askNumber(title, f"{message} ({describeElements(sketch)})")
    if number is None:
        print(f"[DAV] {title} cancelado.")
        return None
    index = int(number)
    if not 1 <= index <= len(sketch.Geometry):
        print(f"[DAV] Error: el boceto tiene {len(sketch.Geometry)} elementos; el {index} no existe.")
        return None
    return index - 1


def askPointPosition(title: str, message: str = "Elegí el punto del elemento", withCenter: bool = True):
    """Ask which point of an element: its start, its end or its centre.

    Returns:
        Sketcher's point number (1 start, 2 end, 3 centre), or None when cancelled.
    """
    options = [
        ("1", "Inicio", ("inicio", "comienzo", "start")),
        ("2", "Final", ("final", "fin", "end")),
    ]
    if withCenter:
        options.append(("3", "Centro", ("centro", "center")))
    choice = askChoice(title, message, options)
    return int(choice) if choice is not None else None


def askPoint(title: str, message: str):
    """Ask X and Y of a point.

    Returns:
        An ``App.Vector`` on the sketch plane, or None when cancelled.
    """
    x = askNumber(title, f"{message}: decí X en mm")
    if x is None:
        return None
    y = askNumber(title, f"{message}: decí Y en mm")
    if y is None:
        return None
    return App.Vector(x, y, 0)

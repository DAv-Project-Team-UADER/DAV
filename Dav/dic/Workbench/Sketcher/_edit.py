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

"""Sketch edits driven by voice: trim, split, extend, fillet, chamfer, mirror, move.

Cada comando pide el boceto de una lista, el elemento por número y los datos
con ventanas numéricas, y llama a la API del boceto sin necesidad de mouse.
"""

import FreeCAD as App

from .._prompts import askChoice, askNumber
from ._elements import askElement, askPoint, askPointPosition, askSketchObject


def _run(doc, sketch, action, done: str) -> None:
    """Run a sketch operation, recompute and report; errors are printed, not raised."""
    try:
        action()
        doc.recompute()
    except Exception as error:
        print(f"[DAV] Error: no se pudo aplicar en '{sketch.Name}': {error}")
        return
    print(f"[DAV] {done} en '{sketch.Name}'.")


def trim_edge() -> None:
    """Trim an element at a point: the part of it that contains the point is removed."""
    doc, sketch = askSketchObject("Recortar")
    if sketch is None:
        return
    geo = askElement(sketch, "Recortar", "Decí el número del elemento a recortar")
    if geo is None:
        return
    point = askPoint("Recortar", "Punto de la parte que se quita")
    if point is None:
        return
    _run(doc, sketch, lambda: sketch.trim(geo, point), f"Elemento {geo + 1} recortado")


def split_edge() -> None:
    """Split an element in two at a point."""
    doc, sketch = askSketchObject("Dividir")
    if sketch is None:
        return
    geo = askElement(sketch, "Dividir", "Decí el número del elemento a dividir")
    if geo is None:
        return
    point = askPoint("Dividir", "Punto de corte")
    if point is None:
        return
    _run(doc, sketch, lambda: sketch.split(geo, point), f"Elemento {geo + 1} dividido")


def extend_edge() -> None:
    """Extend (or shorten, if negative) one end of a line or arc by a distance."""
    doc, sketch = askSketchObject("Extender")
    if sketch is None:
        return
    geo = askElement(sketch, "Extender", "Decí el número del elemento a extender")
    if geo is None:
        return
    end = askPointPosition("Extender", "Elegí el extremo a extender", withCenter=False)
    if end is None:
        return
    distance = askNumber("Extender", "Decí cuántos mm extender (negativo para acortar)")
    if distance is None:
        return
    _run(
        doc, sketch, lambda: sketch.extend(geo, distance, end),
        f"Elemento {geo + 1} extendido {distance} mm",
    )


def _corner(title: str, chamfer: bool) -> None:
    doc, sketch = askSketchObject(title)
    if sketch is None:
        return
    geo = askElement(sketch, title, "Decí el número de un elemento de la esquina")
    if geo is None:
        return
    end = askPointPosition(title, "Elegí el extremo donde está la esquina", withCenter=False)
    if end is None:
        return
    size = askNumber(title, "Decí el radio en mm" if not chamfer else "Decí la distancia del bisel en mm")
    if size is None:
        return
    if size <= 0:
        print(f"[DAV] Error: el valor debe ser mayor que cero (recibido {size}).")
        return
    # trim=1 recorta las líneas hasta el redondeo; createCorner=False no agrega restricciones extra
    _run(
        doc, sketch, lambda: sketch.fillet(geo, end, size, 1, False, chamfer),
        "Bisel aplicado" if chamfer else "Redondeo aplicado",
    )


def fillet_corner() -> None:
    """Round the corner where an element ends meeting another one."""
    _corner("Redondeo", False)


def chamfer_corner() -> None:
    """Bevel (cut at an angle) the corner where an element ends meeting another one."""
    _corner("Bisel", True)


def mirror_elements() -> None:
    """Mirror one element across the horizontal or the vertical axis of the sketch."""
    doc, sketch = askSketchObject("Simetría")
    if sketch is None:
        return
    geo = askElement(sketch, "Simetría", "Decí el número del elemento a reflejar")
    if geo is None:
        return
    axis = askChoice(
        "Simetría",
        "Elegí el eje de simetría",
        [
            ("horizontal", "Eje horizontal (X)", ("horizontal", "equis", "x")),
            ("vertical", "Eje vertical (Y)", ("vertical", "ye", "y")),
        ],
    )
    if axis is None:
        return
    # en un boceto el eje X es la geometría -1 y el eje Y la -2
    reference = -1 if axis == "horizontal" else -2
    _run(doc, sketch, lambda: sketch.addSymmetric([geo], reference), f"Elemento {geo + 1} reflejado")


def move_elements() -> None:
    """Move one element by a dictated distance."""
    doc, sketch = askSketchObject("Mover")
    if sketch is None:
        return
    geo = askElement(sketch, "Mover", "Decí el número del elemento a mover")
    if geo is None:
        return
    dx = askNumber("Mover", "Decí el desplazamiento en X en mm")
    if dx is None:
        return
    dy = askNumber("Mover", "Decí el desplazamiento en Y en mm")
    if dy is None:
        return
    _run(
        doc, sketch, lambda: sketch.addMove([geo], App.Vector(dx, dy, 0)),
        f"Elemento {geo + 1} movido",
    )


def toggle_construction_element() -> None:
    """Turn an element into construction geometry, or back into normal geometry."""
    doc, sketch = askSketchObject("Construcción")
    if sketch is None:
        return
    geo = askElement(sketch, "Construcción", "Decí el número del elemento")
    if geo is None:
        return
    _run(
        doc, sketch, lambda: sketch.toggleConstruction(geo),
        f"Construcción alternada en el elemento {geo + 1}",
    )

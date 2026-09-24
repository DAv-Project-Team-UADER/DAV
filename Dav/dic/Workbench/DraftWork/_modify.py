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

"""Draft modifications driven by voice: the object is chosen from a list.

Los comandos nativos de modificación (mover, rotar, matrices, etc.) esperan
clics de mouse o una selección previa. Acá cada uno pregunta el objeto con
el menú de voz ("avanzar" para cambiar, "okey" para elegir) y sus datos con
las ventanas numéricas, y llama a la API de Draft sin pasar por la vista 3D.
"""

import math

import FreeCAD as App

from .._display import showResult
from .._prompts import askShape
from ._parametric import _activeDoc, _finish, _vec


def _pick(doc, title: str, message: str = "Elegí el objeto"):
    """Ask which object to work on; None when cancelled or there are none."""
    obj = askShape(doc, title, message)
    if obj is None:
        print(f"[DAV] {title} cancelado.")
    return obj


def _pickWire(doc, title: str, message: str = "Elegí la polilínea o curva"):
    """Ask for an object made of points (wire, B-spline, Bézier); None otherwise."""
    obj = _pick(doc, title, message)
    if obj is None:
        return None
    if not hasattr(obj, "Points"):
        print(f"[DAV] Error: '{obj.Name}' no es una polilínea ni una curva de puntos.")
        return None
    return obj


def _done(doc, obj, text: str) -> None:
    """Recompute, show an object that was changed in place and say what happened."""
    doc.recompute()
    showResult(obj)
    print(f"[DAV] {text} '{obj.Name}'.")


def _isDraftObject(obj) -> bool:
    """True for objects created by the Draft workbench (they can be edited in place)."""
    return bool(getattr(getattr(obj, "Proxy", None), "Type", ""))


def clone() -> None:
    """Make a linked clone of an object chosen by voice.

    Example::

        clone()
    """
    doc = _activeDoc()
    if doc is None:
        return
    obj = _pick(doc, "Clonar")
    if obj is None:
        return
    import Draft

    _finish(doc, Draft.make_clone(obj), "clon")


def downgrade() -> None:
    """Break an object down into simpler ones (solid to faces, face to wires...)."""
    _convert("Degradar", "downgrade")


def upgrade() -> None:
    """Join or upgrade an object into a more complex one (wires to a face...)."""
    _convert("Mejorar", "upgrade")


def _convert(title: str, function: str) -> None:
    doc = _activeDoc()
    if doc is None:
        return
    obj = _pick(doc, title)
    if obj is None:
        return
    import Draft

    result = getattr(Draft, function)([obj], delete=False)
    created = result[0] if result else []
    if not created:
        print(f"[DAV] '{obj.Name}' no se puede convertir más.")
        return
    doc.recompute()
    for item in created:
        showResult(item)
    print(f"[DAV] {title}: {len(created)} objeto/s creado/s a partir de '{obj.Name}'.")


def to_sketch() -> None:
    """Convert a Draft object chosen by voice into a Sketcher sketch."""
    doc = _activeDoc()
    if doc is None:
        return
    obj = _pick(doc, "Convertir a boceto")
    if obj is None:
        return
    import Draft

    sketch = Draft.make_sketch([obj], autoconstraints=False)
    if sketch is None:
        print(f"[DAV] Error: '{obj.Name}' no tiene contorno plano para convertir en boceto.")
        return
    _finish(doc, sketch, "boceto")


def move(dx: float, dy: float, dz: float) -> None:
    """Move an object chosen by voice.

    Args:
        dx: Displacement along X, in millimetres.
        dy: Displacement along Y.
        dz: Displacement along Z.

    Example::

        move(10, 0, 0)
    """
    doc = _activeDoc()
    if doc is None:
        return
    obj = _pick(doc, "Mover")
    if obj is None:
        return
    import Draft

    Draft.move(obj, App.Vector(dx, dy, dz), copy=False)
    _done(doc, obj, "Movido")


def rotate(angle: float, cx: float, cy: float) -> None:
    """Rotate an object chosen by voice around a vertical axis.

    Args:
        angle: Rotation angle in degrees, counter-clockwise.
        cx: X of the rotation centre, in millimetres.
        cy: Y of the rotation centre.

    Example::

        rotate(90, 0, 0)
    """
    doc = _activeDoc()
    if doc is None:
        return
    obj = _pick(doc, "Rotar")
    if obj is None:
        return
    import Draft

    Draft.rotate(obj, angle, center=_vec(cx, cy), axis=App.Vector(0, 0, 1), copy=False)
    _done(doc, obj, "Rotado")


def scale(factor: float, cx: float, cy: float) -> None:
    """Scale an object chosen by voice from a centre point.

    Los objetos de Draft se escalan en el lugar; los demás (piezas, cuerpos)
    no admiten escalar sus medidas, así que se crea un clon escalado.

    Args:
        factor: Scale factor, greater than zero (2 doubles the size).
        cx: X of the scale centre, in millimetres.
        cy: Y of the scale centre.

    Example::

        scale(2, 0, 0)
    """
    doc = _activeDoc()
    if doc is None:
        return
    if factor <= 0:
        print(f"[DAV] Error: el factor debe ser mayor que cero (recibido {factor}).")
        return
    obj = _pick(doc, "Escalar")
    if obj is None:
        return
    import Draft

    factors = App.Vector(factor, factor, factor)
    Draft.scale(obj, factors, center=_vec(cx, cy), copy=False, clone=not _isDraftObject(obj))
    _done(doc, obj, "Escalado")


def mirror(x1: float, y1: float, x2: float, y2: float) -> None:
    """Mirror an object chosen by voice across a line given by two points.

    Args:
        x1: X of the first point of the mirror line, in millimetres.
        y1: Y of the first point.
        x2: X of the second point.
        y2: Y of the second point.

    Example::

        mirror(0, 0, 0, 10)
    """
    doc = _activeDoc()
    if doc is None:
        return
    direction = _vec(x2 - x1, y2 - y1)
    if direction.Length == 0:
        print("[DAV] Error: los dos puntos del eje de simetría son iguales.")
        return
    obj = _pick(doc, "Espejo")
    if obj is None:
        return
    # el plano de simetría contiene la línea y el eje Z: su normal es perpendicular a ambos
    normal = direction.cross(App.Vector(0, 0, 1))
    normal.normalize()
    mirrored = doc.addObject("Part::Mirroring", "Mirror")
    mirrored.Source = obj
    mirrored.Base = _vec(x1, y1)
    mirrored.Normal = normal
    _finish(doc, mirrored, "espejo")


def offset(distance: float) -> None:
    """Make a parallel copy of a flat outline at a dictated distance.

    Args:
        distance: Offset in millimetres; positive grows outwards, negative inwards.

    Example::

        offset(5)
    """
    doc = _activeDoc()
    if doc is None:
        return
    if distance == 0:
        print("[DAV] Error: la distancia de desfase no puede ser cero.")
        return
    obj = _pick(doc, "Desfase")
    if obj is None:
        return
    shape = obj.Shape
    if not shape.Faces and not shape.Wires:
        print(f"[DAV] Error: '{obj.Name}' no tiene un contorno plano para desfasar.")
        return
    source = shape.Faces[0] if shape.Faces else shape.Wires[0]
    open_result = not shape.Faces and not source.isClosed()
    try:
        result = source.makeOffset2D(distance, join=0, fill=False, openResult=open_result)
    except Exception as error:
        print(f"[DAV] Error: no se pudo desfasar '{obj.Name}': {error}")
        return
    feature = doc.addObject("Part::Feature", "Offset")
    feature.Shape = result
    _finish(doc, feature, "desfase")


def fillet(radius: float) -> None:
    """Round the corner between two wires or edges chosen by voice.

    Args:
        radius: Fillet radius, in millimetres.

    Example::

        fillet(5)
    """
    doc = _activeDoc()
    if doc is None:
        return
    if radius <= 0:
        print(f"[DAV] Error: el radio debe ser mayor que cero (recibido {radius}).")
        return
    first = _pick(doc, "Redondeo", "Elegí la primera línea")
    if first is None:
        return
    second = _pick(doc, "Redondeo", "Elegí la segunda línea")
    if second is None:
        return
    if first is second:
        print("[DAV] Error: hay que elegir dos líneas distintas.")
        return
    import Draft

    result = Draft.make_fillet([first, second], radius)
    if result is None:
        print("[DAV] Error: no se pudo redondear; las líneas tienen que cortarse o estar cerca.")
        return
    _finish(doc, result, "redondeo")


def cut() -> None:
    """Cut one object with another, both chosen by voice.

    The first object keeps what lies outside the second one; the second stays
    visible, so it can be used as the "front" piece (a chimney behind a roof).

    Example::

        cut()
    """
    doc = _activeDoc()
    if doc is None:
        return
    base = _pick(doc, "Cortar", "Elegí el objeto a cortar")
    if base is None:
        return
    tool = _pick(doc, "Cortar", "Elegí el objeto que corta")
    if tool is None:
        return
    if base is tool:
        print("[DAV] Error: hay que elegir dos objetos distintos.")
        return
    import Draft

    result = Draft.cut(base, tool)
    if result is None:
        print("[DAV] Error: no se pudo cortar.")
        return
    _finish(doc, result, "corte")
    # Draft oculta las dos piezas: la que corta tiene que seguir a la vista
    try:
        tool.ViewObject.Visibility = True
    except Exception:
        pass


def join() -> None:
    """Join two wires chosen by voice into one."""
    doc = _activeDoc()
    if doc is None:
        return
    first = _pickWire(doc, "Unir", "Elegí la primera polilínea")
    if first is None:
        return
    second = _pickWire(doc, "Unir", "Elegí la segunda polilínea")
    if second is None:
        return
    if first is second:
        print("[DAV] Error: hay que elegir dos polilíneas distintas.")
        return
    import Draft

    result = Draft.join_wires([first, second])
    if not result:
        print("[DAV] Error: las polilíneas no comparten un extremo; no se pueden unir.")
        return
    doc.recompute()
    showResult(first)
    print("[DAV] Polilíneas unidas.")


def edit_point(index: int, x: float, y: float) -> None:
    """Move one point of a wire or curve chosen by voice to new coordinates.

    Args:
        index: Point number, starting at 1.
        x: New X, in millimetres.
        y: New Y.

    Example::

        edit_point(2, 15, 10)
    """
    doc = _activeDoc()
    if doc is None:
        return
    obj = _pickWire(doc, "Editar punto")
    if obj is None:
        return
    points = list(obj.Points)
    if not 1 <= index <= len(points):
        print(f"[DAV] Error: '{obj.Name}' tiene {len(points)} puntos; el {index} no existe.")
        return
    points[index - 1] = App.Vector(x, y, points[index - 1].z)
    obj.Points = points
    _done(doc, obj, f"Punto {index} editado en")


def stretch(index: int, dx: float, dy: float) -> None:
    """Stretch a wire by moving one of its points by a dictated distance.

    Args:
        index: Point number, starting at 1.
        dx: Displacement along X, in millimetres.
        dy: Displacement along Y.

    Example::

        stretch(3, 5, 0)
    """
    doc = _activeDoc()
    if doc is None:
        return
    obj = _pickWire(doc, "Estirar")
    if obj is None:
        return
    points = list(obj.Points)
    if not 1 <= index <= len(points):
        print(f"[DAV] Error: '{obj.Name}' tiene {len(points)} puntos; el {index} no existe.")
        return
    points[index - 1] = points[index - 1] + App.Vector(dx, dy, 0)
    obj.Points = points
    _done(doc, obj, f"Punto {index} estirado en")


def slope(percent: float) -> None:
    """Give a wire a constant slope along its length.

    Cada punto sube o baja en Z según la distancia horizontal recorrida desde
    el primero.

    Args:
        percent: Slope in percent (10 rises 10 mm every 100 mm of run).

    Example::

        slope(10)
    """
    doc = _activeDoc()
    if doc is None:
        return
    obj = _pickWire(doc, "Pendiente")
    if obj is None:
        return
    points = list(obj.Points)
    run = 0.0
    result = [points[0]]
    for previous, current in zip(points, points[1:]):
        run += math.hypot(current.x - previous.x, current.y - previous.y)
        result.append(App.Vector(current.x, current.y, points[0].z + run * percent / 100.0))
    obj.Points = result
    _done(doc, obj, "Pendiente aplicada a")


def split_wire(edge: int) -> None:
    """Split a wire in two at the middle of one of its segments.

    Args:
        edge: Segment number, starting at 1.

    Example::

        split_wire(2)
    """
    doc = _activeDoc()
    if doc is None:
        return
    obj = _pickWire(doc, "Dividir")
    if obj is None:
        return
    points = list(obj.Points)
    if not 1 <= edge < len(points):
        print(f"[DAV] Error: '{obj.Name}' tiene {len(points) - 1} segmentos; el {edge} no existe.")
        return
    import Draft

    middle = (points[edge - 1] + points[edge]) * 0.5
    result = Draft.split(obj, middle, edge)
    if result is None:
        print("[DAV] Error: no se pudo dividir la polilínea (solo funciona con polilíneas abiertas).")
        return
    doc.recompute()
    showResult(result)
    print(f"[DAV] '{obj.Name}' dividida en el segmento {edge}.")


def trim_extend(distance: float) -> None:
    """Extend (or trim, if negative) the last segment of a wire by a distance.

    Args:
        distance: Millimetres to add to the end; negative shortens it.

    Example::

        trim_extend(10)
    """
    doc = _activeDoc()
    if doc is None:
        return
    obj = _pickWire(doc, "Recortar o extender")
    if obj is None:
        return
    points = list(obj.Points)
    if len(points) < 2:
        print(f"[DAV] Error: '{obj.Name}' necesita al menos dos puntos.")
        return
    direction = points[-1] - points[-2]
    if distance < 0 and -distance >= direction.Length:
        print("[DAV] Error: el recorte es mayor que el último segmento.")
        return
    direction.normalize()
    points[-1] = points[-1] + direction * distance
    obj.Points = points
    _done(doc, obj, "Extremo ajustado en")


def wire_to_bspline() -> None:
    """Replace a wire chosen by voice with a smooth B-spline through its points."""
    doc = _activeDoc()
    if doc is None:
        return
    obj = _pickWire(doc, "Convertir a curva")
    if obj is None:
        return
    import Draft

    closed = bool(getattr(obj, "Closed", False))
    spline = Draft.make_bspline(list(obj.Points), closed=closed)
    obj.Visibility = False
    _finish(doc, spline, "curva B-spline")


def shape_2d_view() -> None:
    """Make a flat 2D projection of a 3D object chosen by voice."""
    doc = _activeDoc()
    if doc is None:
        return
    obj = _pick(doc, "Vista 2D", "Elegí el objeto 3D")
    if obj is None:
        return
    import Draft

    _finish(doc, Draft.make_shape2dview(obj), "vista 2D")


def highlight_subelements() -> None:
    """Show the vertices and edges of an object chosen by voice."""
    doc = _activeDoc()
    if doc is None:
        return
    obj = _pick(doc, "Resaltar subelementos")
    if obj is None:
        return
    import FreeCADGui as Gui

    Gui.Selection.clearSelection()
    Gui.Selection.addSelection(obj)
    Gui.runCommand("Draft_SubelementHighlight", 0)


def circular_array(radial: float, tangential: float, number: int) -> None:
    """Repeat an object chosen by voice in concentric rings around the origin.

    Args:
        radial: Distance between rings, in millimetres.
        tangential: Distance between copies inside a ring.
        number: Number of rings.

    Example::

        circular_array(30, 20, 3)
    """
    doc = _activeDoc()
    if doc is None:
        return
    if radial <= 0 or tangential <= 0 or number < 1:
        print("[DAV] Error: las distancias deben ser mayores que cero y debe haber al menos 1 anillo.")
        return
    obj = _pick(doc, "Matriz circular")
    if obj is None:
        return
    import Draft

    _finish(doc, Draft.make_circular_array(obj, radial, tangential, number), "matriz circular")


def ortho_array(dx: float, dy: float, countX: int, countY: int) -> None:
    """Repeat an object chosen by voice in a rectangular grid.

    Args:
        dx: Distance between copies along X, in millimetres.
        dy: Distance between copies along Y.
        countX: Number of copies along X.
        countY: Number of copies along Y.

    Example::

        ortho_array(20, 20, 3, 2)
    """
    doc = _activeDoc()
    if doc is None:
        return
    if countX < 1 or countY < 1:
        print("[DAV] Error: hace falta al menos 1 copia en cada dirección.")
        return
    obj = _pick(doc, "Matriz ortogonal")
    if obj is None:
        return
    import Draft

    result = Draft.make_ortho_array2d(
        obj, App.Vector(dx, 0, 0), App.Vector(0, dy, 0), countX, countY
    )
    _finish(doc, result, "matriz ortogonal")


def polar_array(number: int, angle: float, cx: float, cy: float) -> None:
    """Repeat an object chosen by voice around a centre point.

    Args:
        number: Number of copies, at least 2.
        angle: Total angle swept, in degrees (360 closes the circle).
        cx: X of the centre, in millimetres.
        cy: Y of the centre.

    Example::

        polar_array(6, 360, 0, 0)
    """
    doc = _activeDoc()
    if doc is None:
        return
    if number < 2 or angle == 0:
        print("[DAV] Error: hacen falta al menos 2 copias y un ángulo distinto de cero.")
        return
    obj = _pick(doc, "Matriz polar")
    if obj is None:
        return
    import Draft

    _finish(doc, Draft.make_polar_array(obj, number, angle, _vec(cx, cy)), "matriz polar")


def _pathArray(count: int, useLink: bool, title: str) -> None:
    doc = _activeDoc()
    if doc is None:
        return
    if count < 2:
        print("[DAV] Error: hacen falta al menos 2 copias.")
        return
    base = _pick(doc, title, "Elegí el objeto a repetir")
    if base is None:
        return
    path = _pick(doc, title, "Elegí la trayectoria")
    if path is None:
        return
    if base is path:
        print("[DAV] Error: la trayectoria no puede ser el mismo objeto.")
        return
    import Draft

    _finish(doc, Draft.make_path_array(base, path, count, use_link=useLink), "matriz por trayectoria")


def path_array(count: int) -> None:
    """Repeat an object chosen by voice along a path chosen by voice.

    Args:
        count: Number of copies, at least 2.

    Example::

        path_array(5)
    """
    _pathArray(count, False, "Matriz por trayectoria")


def path_link_array(count: int) -> None:
    """Same as ``path_array`` but the copies are lightweight links.

    Args:
        count: Number of copies, at least 2.

    Example::

        path_link_array(5)
    """
    _pathArray(count, True, "Enlace por trayectoria")


def _pointArray(useLink: bool, title: str) -> None:
    doc = _activeDoc()
    if doc is None:
        return
    base = _pick(doc, title, "Elegí el objeto a repetir")
    if base is None:
        return
    points = _pick(doc, title, "Elegí el objeto que tiene los puntos")
    if points is None:
        return
    if base is points:
        print("[DAV] Error: los puntos no pueden ser el mismo objeto.")
        return
    import Draft

    _finish(doc, Draft.make_point_array(base, points, use_link=useLink), "matriz por puntos")


def point_array() -> None:
    """Repeat an object chosen by voice at the points of another object."""
    _pointArray(False, "Matriz por puntos")


def point_link_array() -> None:
    """Same as ``point_array`` but the copies are lightweight links."""
    _pointArray(True, "Enlace por puntos")


def facebinder(face: int) -> None:
    """Create a surface bound to one face of an object chosen by voice.

    Args:
        face: Face number, starting at 1.

    Example::

        facebinder(3)
    """
    doc = _activeDoc()
    if doc is None:
        return
    if face < 1:
        print("[DAV] Error: el número de cara empieza en 1.")
        return
    obj = _pick(doc, "Unir caras", "Elegí el objeto que tiene la cara")
    if obj is None:
        return
    if face > len(obj.Shape.Faces):
        print(f"[DAV] Error: '{obj.Name}' tiene {len(obj.Shape.Faces)} caras; la {face} no existe.")
        return
    import Draft

    _finish(doc, Draft.make_facebinder([(obj, (f"Face{face}",))]), "unión de caras")

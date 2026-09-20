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

"""Parametric Draft commands: every value is asked with a voice window.

Igual que el banco de croquis: cada argumento tipado (``float``, ``int``,
``str``) sin valor por defecto hace que ParameterCollector abra una ventana
de voz por dato, en lugar de lanzar el comando nativo que necesita mouse.
"""

import math

import FreeCAD as App

try:
    from createobjects import CreateObjects
except ImportError:
    from selection.createobjects import CreateObjects
from .._display import showResult


def _vec(x: float, y: float) -> App.Vector:
    """Return a point on the XY plane (Z = 0)."""
    return App.Vector(x, y, 0)


def _placement(x: float, y: float, rotation=None) -> App.Placement:
    """Return a placement at (x, y) on the XY plane."""
    return App.Placement(_vec(x, y), rotation or App.Rotation())


def _activeDoc():
    """Return the active document, printing an error when there is none."""
    doc = App.activeDocument()
    if doc is None:
        print("[DAV] Error: no hay documento activo.")
    return doc


def _finish(doc, obj, label: str) -> None:
    """Recompute, show and register in the DAV tree the Draft object just made."""
    doc.recompute()
    showResult(obj)
    try:
        CreateObjects(ObjectName=obj.Name, Is3D=False).Execute()
    except Exception as error:
        print(f"[DAV] No se pudo registrar {obj.Name}: {error}")
    print(f"[DAV] Creado {label} '{obj.Name}'.")


def _circumcircle(p1, p2, p3):
    """Return ``(center, radius)`` of the circle through three points, or None."""
    (x1, y1), (x2, y2), (x3, y3) = p1, p2, p3
    d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    # puntos alineados: no hay circunferencia única
    if abs(d) < 1e-9:
        return None
    sq1, sq2, sq3 = x1 * x1 + y1 * y1, x2 * x2 + y2 * y2, x3 * x3 + y3 * y3
    ux = (sq1 * (y2 - y3) + sq2 * (y3 - y1) + sq3 * (y1 - y2)) / d
    uy = (sq1 * (x3 - x2) + sq2 * (x1 - x3) + sq3 * (x2 - x1)) / d
    return (ux, uy), math.hypot(x1 - ux, y1 - uy)


def _angle(center, point) -> float:
    """Angle in degrees of point around center, in [0, 360)."""
    return math.degrees(math.atan2(point[1] - center[1], point[0] - center[0])) % 360


def circle_by_center(x: float, y: float, radius: float) -> None:
    """Create a Draft circle from its center and radius.

    Args:
        x: Center X coordinate, in millimetres.
        y: Center Y coordinate, in millimetres.
        radius: Radius in millimetres. Must be greater than zero.

    Example::

        circle_by_center(0, 0, 25)
    """
    doc = _activeDoc()
    if doc is None:
        return
    if radius <= 0:
        print(f"[DAV] Error: el radio debe ser mayor que cero (recibido {radius}).")
        return
    import Draft

    _finish(doc, Draft.make_circle(radius, placement=_placement(x, y)), "círculo")


def arc_by_center(x: float, y: float, radius: float, startAngle: float, endAngle: float) -> None:
    """Create a Draft arc from its center, radius and angles.

    Args:
        x: Center X coordinate, in millimetres.
        y: Center Y coordinate, in millimetres.
        radius: Radius in millimetres. Must be greater than zero.
        startAngle: Start angle in degrees, counter-clockwise from the X axis.
        endAngle: End angle in degrees. Must differ from the start angle.

    Example::

        arc_by_center(0, 0, 25, 0, 90)
    """
    doc = _activeDoc()
    if doc is None:
        return
    if radius <= 0:
        print(f"[DAV] Error: el radio debe ser mayor que cero (recibido {radius}).")
        return
    if (endAngle - startAngle) % 360 == 0:
        print("[DAV] Error: el ángulo final debe ser distinto del inicial.")
        return
    import Draft

    obj = Draft.make_circle(
        radius, placement=_placement(x, y), startangle=startAngle, endangle=endAngle
    )
    _finish(doc, obj, "arco")


def arc_by_3_points(x1: float, y1: float, x2: float, y2: float, x3: float, y3: float) -> None:
    """Create a Draft arc from its two ends and a point in between.

    Args:
        x1: X of the start point, in millimetres.
        y1: Y of the start point.
        x2: X of a point on the arc between both ends.
        y2: Y of that point.
        x3: X of the end point.
        y3: Y of the end point.

    Example::

        arc_by_3_points(10, 0, 0, 10, -10, 0)
    """
    doc = _activeDoc()
    if doc is None:
        return
    p1, p2, p3 = (x1, y1), (x2, y2), (x3, y3)
    found = _circumcircle(p1, p2, p3)
    if found is None:
        print("[DAV] Error: los 3 puntos están alineados, no definen un arco.")
        return
    center, radius = found
    # Draft dibuja siempre en sentido antihorario: si p1→p2→p3 gira al revés se invierten los extremos
    turn = (x2 - x1) * (y3 - y2) - (y2 - y1) * (x3 - x2)
    if turn > 0:
        start, end = _angle(center, p1), _angle(center, p3)
    else:
        start, end = _angle(center, p3), _angle(center, p1)
    import Draft

    obj = Draft.make_circle(
        radius, placement=_placement(*center), startangle=start, endangle=end
    )
    _finish(doc, obj, "arco")


def ellipse_by_center(x: float, y: float, majorRadius: float, minorRadius: float) -> None:
    """Create a Draft ellipse from its center and both semi-axes.

    Args:
        x: Center X coordinate, in millimetres.
        y: Center Y coordinate, in millimetres.
        majorRadius: Semi-axis along X, in millimetres.
        minorRadius: Semi-axis along Y, in millimetres.

    Example::

        ellipse_by_center(0, 0, 30, 15)
    """
    doc = _activeDoc()
    if doc is None:
        return
    if majorRadius <= 0 or minorRadius <= 0:
        print("[DAV] Error: los dos radios deben ser mayores que cero.")
        return
    import Draft

    # Draft exige el semieje mayor primero: si se dictó al revés se gira la elipse 90°
    if majorRadius >= minorRadius:
        major, minor, rotation = majorRadius, minorRadius, App.Rotation()
    else:
        major, minor, rotation = minorRadius, majorRadius, App.Rotation(App.Vector(0, 0, 1), 90)
    obj = Draft.make_ellipse(major, minor, placement=_placement(x, y, rotation))
    _finish(doc, obj, "elipse")


def rectangle_by_corners(x1: float, y1: float, x2: float, y2: float) -> None:
    """Create a Draft rectangle from two opposite corners.

    Args:
        x1: X of the first corner, in millimetres.
        y1: Y of the first corner.
        x2: X of the opposite corner.
        y2: Y of the opposite corner.

    Example::

        rectangle_by_corners(0, 0, 40, 20)
    """
    doc = _activeDoc()
    if doc is None:
        return
    length, height = abs(x2 - x1), abs(y2 - y1)
    if length == 0 or height == 0:
        print("[DAV] Error: el rectángulo necesita base y altura distintas de cero.")
        return
    import Draft

    obj = Draft.make_rectangle(length, height, placement=_placement(min(x1, x2), min(y1, y2)))
    _finish(doc, obj, "rectángulo")


def polygon_by_center(x: float, y: float, sides: int, radius: float) -> None:
    """Create a regular Draft polygon inscribed in a circle.

    Args:
        x: Center X coordinate, in millimetres.
        y: Center Y coordinate, in millimetres.
        sides: Number of sides, at least 3.
        radius: Radius of the circumscribed circle, in millimetres.

    Example::

        polygon_by_center(0, 0, 6, 20)
    """
    doc = _activeDoc()
    if doc is None:
        return
    if sides < 3 or radius <= 0:
        print("[DAV] Error: hacen falta al menos 3 lados y un radio mayor que cero.")
        return
    import Draft

    obj = Draft.make_polygon(sides, radius=radius, placement=_placement(x, y))
    _finish(doc, obj, "polígono")


def point_by_coords(x: float, y: float) -> None:
    """Create a Draft point on the XY plane.

    Args:
        x: X coordinate, in millimetres.
        y: Y coordinate, in millimetres.

    Example::

        point_by_coords(10, 5)
    """
    doc = _activeDoc()
    if doc is None:
        return
    import Draft

    _finish(doc, Draft.make_point(x, y, 0), "punto")


def wire_by_points(x1: float, y1: float, x2: float, y2: float, x3: float, y3: float) -> None:
    """Create an open Draft polyline through three points.

    Args:
        x1: X of the first point, in millimetres.
        y1: Y of the first point.
        x2: X of the second point.
        y2: Y of the second point.
        x3: X of the third point.
        y3: Y of the third point.

    Example::

        wire_by_points(0, 0, 20, 0, 20, 10)
    """
    doc = _activeDoc()
    if doc is None:
        return
    import Draft

    obj = Draft.make_wire([_vec(x1, y1), _vec(x2, y2), _vec(x3, y3)], closed=False)
    _finish(doc, obj, "polilínea")


def bezier_by_points(x1: float, y1: float, x2: float, y2: float, x3: float, y3: float) -> None:
    """Create a quadratic Bezier curve from three control points.

    Args:
        x1: X of the start point, in millimetres.
        y1: Y of the start point.
        x2: X of the control point.
        y2: Y of the control point.
        x3: X of the end point.
        y3: Y of the end point.

    Example::

        bezier_by_points(0, 0, 10, 20, 20, 0)
    """
    doc = _activeDoc()
    if doc is None:
        return
    import Draft

    obj = Draft.make_bezcurve([_vec(x1, y1), _vec(x2, y2), _vec(x3, y3)], degree=2)
    _finish(doc, obj, "curva Bézier")


def cubic_by_points(
    x1: float, y1: float, x2: float, y2: float, x3: float, y3: float, x4: float, y4: float
) -> None:
    """Create a cubic Bezier curve from four control points.

    Args:
        x1: X of the start point, in millimetres.
        y1: Y of the start point.
        x2: X of the first control point.
        y2: Y of the first control point.
        x3: X of the second control point.
        y3: Y of the second control point.
        x4: X of the end point.
        y4: Y of the end point.

    Example::

        cubic_by_points(0, 0, 5, 20, 15, 20, 20, 0)
    """
    doc = _activeDoc()
    if doc is None:
        return
    import Draft

    points = [_vec(x1, y1), _vec(x2, y2), _vec(x3, y3), _vec(x4, y4)]
    _finish(doc, Draft.make_bezcurve(points, degree=3), "curva Bézier cúbica")


def bspline_by_points(
    x1: float, y1: float, x2: float, y2: float, x3: float, y3: float, x4: float, y4: float
) -> None:
    """Create a B-spline passing through four points.

    Args:
        x1: X of the first point, in millimetres.
        y1: Y of the first point.
        x2: X of the second point.
        y2: Y of the second point.
        x3: X of the third point.
        y3: Y of the third point.
        x4: X of the fourth point.
        y4: Y of the fourth point.

    Example::

        bspline_by_points(0, 0, 10, 15, 20, 5, 30, 20)
    """
    doc = _activeDoc()
    if doc is None:
        return
    import Draft

    points = [_vec(x1, y1), _vec(x2, y2), _vec(x3, y3), _vec(x4, y4)]
    _finish(doc, Draft.make_bspline(points, closed=False), "B-spline")


def text_at(content: str, x: float, y: float) -> None:
    """Create a Draft text annotation.

    Args:
        content: The text to write.
        x: X of the text position, in millimetres.
        y: Y of the text position.

    Example::

        text_at("Pieza A", 0, 0)
    """
    doc = _activeDoc()
    if doc is None:
        return
    if not content.strip():
        print("[DAV] Error: el texto está vacío.")
        return
    import Draft

    _finish(doc, Draft.make_text([content], placement=_placement(x, y)), "texto")


def linear_dimension(x1: float, y1: float, x2: float, y2: float) -> None:
    """Create a linear Draft dimension between two points.

    Args:
        x1: X of the first point, in millimetres.
        y1: Y of the first point.
        x2: X of the second point.
        y2: Y of the second point.

    Example::

        linear_dimension(0, 0, 40, 0)
    """
    doc = _activeDoc()
    if doc is None:
        return
    if (x1, y1) == (x2, y2):
        print("[DAV] Error: los dos puntos de la cota son iguales.")
        return
    import Draft

    _finish(doc, Draft.make_linear_dimension(_vec(x1, y1), _vec(x2, y2)), "cota")

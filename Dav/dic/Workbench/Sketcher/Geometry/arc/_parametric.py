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
# SPDX-License-Identifier: GPL-3.0-or-later

"""Parametric geometry commands for Validator (numbers and strings)."""

from __future__ import annotations

import math

import FreeCAD as App
import Part


def create_by_center(
    x: float,
    y: float,
    radius: float,
    angle_start: float,
    angle_end: float,
    label: str = "Arc",
) -> None:
    """Create a Part arc from a dictated center, radius and angle sweep.

    Angles are dictated in degrees (the unit used by FreeCAD's own dialogs) and
    converted to radians internally. The arc runs counter-clockwise from
    angle_start to angle_end.

    Args:
        x: Center X coordinate, in millimetres.
        y: Center Y coordinate, in millimetres.
        radius: Arc radius, in millimetres. Must be greater than zero.
        angle_start: Start angle, in degrees.
        angle_end: End angle, in degrees. Must differ from angle_start.
        label: Visible label for the created object.

    Example::

        create_by_center(0, 0, 25, 0, 90)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[geometry.arc] Error: no active document.")
        return

    if radius <= 0:
        print(f"[geometry.arc] Error: radius must be greater than zero (got {radius}).")
        return

    # un barrido multiplo de 360 no deja arco: Part.ArcOfCircle falla o da vacio
    if (angle_end - angle_start) % 360 == 0:
        print("[geometry.arc] Error: start and end angles describe an empty sweep.")
        return

    circle = Part.Circle(App.Vector(x, y, 0), App.Vector(0, 0, 1), radius)
    arc_geo = Part.ArcOfCircle(
        circle,
        math.radians(angle_start),
        math.radians(angle_end),
    )

    sketch = getattr(doc, "ActiveObject", None)
    if sketch and getattr(sketch, "TypeId", "") == "Sketcher::SketchObject":
        sketch.addGeometry(arc_geo, False)
        doc.recompute()
        print(
            f"[geometry.arc] Added arc to sketch at ({x},{y}) radius {radius} "
            f"from {angle_start} to {angle_end} degrees"
        )
        return

    safe_name = "".join(ch for ch in label if ch.isalnum()) or "Arc"
    shape = arc_geo.toShape()

    feature = doc.addObject("Part::Feature", safe_name)
    feature.Label = label
    feature.Shape = shape
    doc.recompute()
    print(
        f"[geometry.arc] Created '{label}' at ({x},{y}) radius {radius} "
        f"from {angle_start} to {angle_end} degrees"
    )


def create_by_3points(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    x3: float,
    y3: float,
    label: str = "Arc",
) -> None:
    """Create an arc passing through 3 points (p1: start, p2: midpoint/minimum, p3: end)."""
    doc = App.activeDocument()
    if doc is None:
        print("[geometry.arc] Error: no active document.")
        return

    p1 = App.Vector(x1, y1, 0)
    p2 = App.Vector(x2, y2, 0)
    p3 = App.Vector(x3, y3, 0)

    try:
        arc_geo = Part.ArcOfCircle(p1, p2, p3)
    except Exception as exc:
        print(f"[geometry.arc] Error creating 3-point arc: {exc}")
        return

    sketch = getattr(doc, "ActiveObject", None)
    if sketch and getattr(sketch, "TypeId", "") == "Sketcher::SketchObject":
        sketch.addGeometry(arc_geo, False)
        doc.recompute()
        print(
            f"[geometry.arc] Added 3-point arc to sketch through ({x1},{y1}), ({x2},{y2}), ({x3},{y3})"
        )
        return

    safe_name = "".join(ch for ch in label if ch.isalnum()) or "Arc"
    shape = arc_geo.toShape()
    feature = doc.addObject("Part::Feature", safe_name)
    feature.Label = label
    feature.Shape = shape
    doc.recompute()
    print(
        f"[geometry.arc] Created 3-point arc '{label}' through ({x1},{y1}), ({x2},{y2}), ({x3},{y3})"
    )

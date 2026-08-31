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

    safe_name = "".join(ch for ch in label if ch.isalnum()) or "Arc"
    circle = Part.Circle(App.Vector(x, y, 0), App.Vector(0, 0, 1), radius)
    shape = Part.ArcOfCircle(
        circle,
        math.radians(angle_start),
        math.radians(angle_end),
    ).toShape()

    feature = doc.addObject("Part::Feature", safe_name)
    feature.Label = label
    feature.Shape = shape
    doc.recompute()
    print(
        f"[geometry.arc] Created '{label}' at ({x},{y}) radius {radius} "
        f"from {angle_start} to {angle_end} degrees"
    )

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

"""Parametric arc-slot commands for Validator (numbers and strings)."""

from __future__ import annotations

import math

import FreeCAD as App
import Part


def _point(cx: float, cy: float, radius: float, angle_deg: float) -> App.Vector:
    """Return a point on a radius at a given angle (degrees), in the XY plane."""
    a = math.radians(angle_deg)
    return App.Vector(cx + radius * math.cos(a), cy + radius * math.sin(a), 0)


def _annular_arc(
    cx: float,
    cy: float,
    radius: float,
    angle_start: float,
    angle_end: float,
) -> Part.Edge:
    """Build the counter-clockwise arc of a radius between two angles."""
    circle = Part.Circle(
        App.Vector(cx, cy, 0), App.Vector(0, 0, 1), radius
    )
    return Part.ArcOfCircle(
        circle, math.radians(angle_start), math.radians(angle_end)
    ).toShape()


def _create_arc_slot(
    cx: float,
    cy: float,
    radius: float,
    angle_start: float,
    angle_end: float,
    width: float,
    flat_ends: bool,
    label: str,
) -> None:
    """Core arc-slot builder shared by the rounded and flat variants."""
    doc = App.activeDocument()
    if doc is None:
        print("[geometry.arc_slot] Error: no active document.")
        return

    if radius <= 0:
        print(f"[geometry.arc_slot] Error: radius must be greater than zero (got {radius}).")
        return
    if width <= 0:
        print(f"[geometry.arc_slot] Error: width must be greater than zero (got {width}).")
        return
    if radius - width / 2.0 <= 0:
        print(
            "[geometry.arc_slot] Error: width is too large "
            f"(inner radius {radius - width / 2.0:.3f} <= 0)."
        )
        return
    sweep = angle_end - angle_start
    if sweep <= 0:
        print("[geometry.arc_slot] Error: angle_end must be greater than angle_start.")
        return
    if sweep >= 180:
        print(
            "[geometry.arc_slot] Error: the angle sweep must be less than 180 "
            f"degrees (got {sweep})."
        )
        return

    mid_angle = (angle_start + angle_end) / 2.0
    r_in = radius - width / 2.0
    r_out = radius + width / 2.0

    p_in_1 = _point(cx, cy, r_in, angle_start)
    p_in_2 = _point(cx, cy, r_in, angle_end)
    p_out_1 = _point(cx, cy, r_out, angle_start)
    p_out_2 = _point(cx, cy, r_out, angle_end)

    outer_arc = _annular_arc(cx, cy, r_out, angle_start, angle_end)
    # los tres puntos sobre la circunferencia interna definen el arco de
    # contorno: se recorre en sentido inverso (de angle_end a angle_start)
    p_in_mid = _point(cx, cy, r_in, mid_angle)
    inner_arc_3p = Part.Arc(p_in_2, p_in_mid, p_in_1).toShape()

    if flat_ends:
        edges = [
            outer_arc,
            Part.makeLine(p_out_2, p_in_2),
            inner_arc_3p,
            Part.makeLine(p_in_1, p_out_1),
        ]
    else:
        perp_end = App.Vector(
            -math.sin(math.radians(angle_end)),
            math.cos(math.radians(angle_end)),
            0,
        )
        perp_start = App.Vector(
            -math.sin(math.radians(angle_start)),
            math.cos(math.radians(angle_start)),
            0,
        )
        cap_end_center = App.Vector(
            cx + radius * math.cos(math.radians(angle_end)),
            cy + radius * math.sin(math.radians(angle_end)),
            0,
        )
        cap_start_center = App.Vector(
            cx + radius * math.cos(math.radians(angle_start)),
            cy + radius * math.sin(math.radians(angle_start)),
            0,
        )
        cap_end = Part.Arc(
            p_out_2,
            cap_end_center + perp_end.multiply(width / 2.0),
            p_in_2,
        ).toShape()
        cap_start = Part.Arc(
            p_in_1,
            cap_start_center - perp_start.multiply(width / 2.0),
            p_out_1,
        ).toShape()
        edges = [outer_arc, cap_end, inner_arc_3p, cap_start]

    wire = Part.Wire(edges)
    try:
        shape = Part.Face(wire)
    except Exception:
        # si el contorno cerrado por algun motivo no forma cara, se devuelve
        # el wire: la geometria se ve igual en la vista 3D
        shape = wire

    safe_name = "".join(ch for ch in label if ch.isalnum()) or "ArcSlot"
    feature = doc.addObject("Part::Feature", safe_name)
    feature.Label = label
    feature.Shape = shape
    doc.recompute()
    print(
        f"[geometry.arc_slot] Created '{label}' at ({cx},{cy}) radius {radius} "
        f"from {angle_start} to {angle_end} degrees width {width} "
        f"({'flat' if flat_ends else 'rounded'} ends)"
    )


def create_arc_slot_rounded(
    cx: float,
    cy: float,
    radius: float,
    angle_start: float,
    angle_end: float,
    width: float,
    label: str = "ArcSlot",
) -> None:
    """Create an arc slot with rounded ends from dictated numeric input.

    Every numeric argument is a required float, so ParameterCollector opens one
    voice prompt per value (same window as "línea por puntos").

    Args:
        cx: Center X coordinate, in millimetres.
        cy: Center Y coordinate, in millimetres.
        radius: Middle radius of the slot, in millimetres. Must be greater
            than half the width.
        angle_start: Start angle, in degrees.
        angle_end: End angle, in degrees. The sweep (end - start) must be
            between 0 and 180 degrees.
        width: Slot thickness (outer radius minus inner radius), in
            millimetres. Must be positive and less than twice ``radius``.
        label: Visible label for the created object.

    Example::

        create_arc_slot_rounded(0, 0, 30, 0, 90, 10)
    """
    _create_arc_slot(
        cx, cy, radius, angle_start, angle_end, width, flat_ends=False, label=label
    )


def create_arc_slot_flat(
    cx: float,
    cy: float,
    radius: float,
    angle_start: float,
    angle_end: float,
    width: float,
    label: str = "ArcSlot",
) -> None:
    """Create an arc slot with flat (square) ends from dictated numeric input.

    Same arguments and voice prompts as create_arc_slot_rounded, but the ends
    are radial straight segments instead of rounded caps.

    Args:
        cx: Center X coordinate, in millimetres.
        cy: Center Y coordinate, in millimetres.
        radius: Middle radius of the slot, in millimetres.
        angle_start: Start angle, in degrees.
        angle_end: End angle, in degrees. The sweep must be between 0 and 180.
        width: Slot thickness, in millimetres.
        label: Visible label for the created object.

    Example::

        create_arc_slot_flat(0, 0, 30, 0, 90, 10)
    """
    _create_arc_slot(
        cx, cy, radius, angle_start, angle_end, width, flat_ends=True, label=label
    )
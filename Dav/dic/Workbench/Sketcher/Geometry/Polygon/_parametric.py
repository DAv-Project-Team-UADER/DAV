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


def create_regular(
    sides: int,
    x: float,
    y: float,
    radius: float,
    label: str = "Polygon",
) -> None:
    """Create a regular Part polygon inscribed in a dictated circle.

    sides is an int, so it is collected with IntegerInputPrompt while the
    remaining values use FloatInputPrompt. The first vertex sits on the
    positive X axis, matching FreeCAD's own regular polygon tool.

    Args:
        sides: Number of sides. Must be 3 or more.
        x: Center X coordinate, in millimetres.
        y: Center Y coordinate, in millimetres.
        radius: Circumscribed circle radius, in millimetres.
        label: Visible label for the created object.

    Example::

        create_regular(6, 0, 0, 25)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[geometry.polygon] Error: no active document.")
        return

    if sides < 3:
        print(f"[geometry.polygon] Error: a polygon needs at least 3 sides (got {sides}).")
        return
    if radius <= 0:
        print(f"[geometry.polygon] Error: radius must be greater than zero (got {radius}).")
        return

    step = 2 * math.pi / sides
    vertices = [
        App.Vector(x + radius * math.cos(i * step), y + radius * math.sin(i * step), 0)
        for i in range(sides)
    ]

    safe_name = "".join(ch for ch in label if ch.isalnum()) or "Polygon"
    shape = Part.makePolygon(vertices + [vertices[0]])

    feature = doc.addObject("Part::Feature", safe_name)
    feature.Label = label
    feature.Shape = shape
    doc.recompute()
    print(
        f"[geometry.polygon] Created '{label}' with {sides} sides "
        f"at ({x},{y}) radius {radius}"
    )

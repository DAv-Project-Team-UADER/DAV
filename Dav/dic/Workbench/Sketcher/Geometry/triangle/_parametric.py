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

"""Parametric geometry commands for the triangle (dictated coordinates)."""

from __future__ import annotations

import FreeCAD as App
import Part

from .._sketch import addToEditedSketch


def create_by_vertices(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    x3: float,
    y3: float,
    label: str = "Triangle",
) -> None:
    """Create a closed triangle from three dictated vertices.

    Args:
        x1: First vertex X coordinate, in millimetres.
        y1: First vertex Y coordinate, in millimetres.
        x2: Second vertex X coordinate, in millimetres.
        y2: Second vertex Y coordinate, in millimetres.
        x3: Third vertex X coordinate, in millimetres.
        y3: Third vertex Y coordinate, in millimetres.
        label: Visible label for the created object.

    Example::

        create_by_vertices(0, 20, 40, 20, 20, 40)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[geometry.triangle] Error: no active document.")
        return

    # vertices alineados dan un triangulo degenerado (area cero)
    area2 = (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)
    if area2 == 0:
        print("[geometry.triangle] Error: the three vertices must not be collinear.")
        return

    vertices = [
        App.Vector(x1, y1, 0),
        App.Vector(x2, y2, 0),
        App.Vector(x3, y3, 0),
    ]
    shape = Part.makePolygon(vertices + [vertices[0]])

    if addToEditedSketch(doc, shape):
        return
    safe_name = "".join(ch for ch in label if ch.isalnum()) or "Triangle"
    feature = doc.addObject("Part::Feature", safe_name)
    feature.Label = label
    feature.Shape = shape
    doc.recompute()
    print(
        f"[geometry.triangle] Created '{label}' with vertices "
        f"({x1},{y1}), ({x2},{y2}), ({x3},{y3})"
    )

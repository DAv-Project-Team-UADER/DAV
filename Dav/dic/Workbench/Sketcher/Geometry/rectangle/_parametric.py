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

import FreeCAD as App
import Part


def create_by_corners(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    label: str = "Rectangle",
) -> None:
    """Create a closed Part rectangle from two dictated opposite corners.

    The corners may be given in any order; the rectangle is built from the
    resulting bounding box, so (10,10)-(0,0) and (0,0)-(10,10) are equivalent.

    Args:
        x1: First corner X coordinate, in millimetres.
        y1: First corner Y coordinate, in millimetres.
        x2: Opposite corner X coordinate, in millimetres.
        y2: Opposite corner Y coordinate, in millimetres.
        label: Visible label for the created object.

    Example::

        create_by_corners(0, 0, 40, 20)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[geometry.rectangle] Error: no active document.")
        return

    # esquinas coincidentes en un eje dan un rectangulo degenerado (una linea)
    if x1 == x2 or y1 == y2:
        print("[geometry.rectangle] Error: corners must differ on both axes.")
        return

    left, right = min(x1, x2), max(x1, x2)
    bottom, top = min(y1, y2), max(y1, y2)

    corners = [
        App.Vector(left, bottom, 0),
        App.Vector(right, bottom, 0),
        App.Vector(right, top, 0),
        App.Vector(left, top, 0),
    ]

    safe_name = "".join(ch for ch in label if ch.isalnum()) or "Rectangle"
    shape = Part.makePolygon(corners + [corners[0]])

    feature = doc.addObject("Part::Feature", safe_name)
    feature.Label = label
    feature.Shape = shape
    doc.recompute()
    print(
        f"[geometry.rectangle] Created '{label}' from ({left},{bottom}) to ({right},{top})"
    )

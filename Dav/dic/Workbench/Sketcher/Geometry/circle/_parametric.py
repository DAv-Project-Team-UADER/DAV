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


def create_by_center(
    x: float,
    y: float,
    radius: float,
    label: str = "Circle",
) -> None:
    """Create a Part circle from a dictated center and radius.

    Mirrors line.create_by_points: every argument is a required float, so
    ParameterCollector raises one voice prompt per coordinate.

    Args:
        x: Center X coordinate, in millimetres.
        y: Center Y coordinate, in millimetres.
        radius: Circle radius, in millimetres. Must be greater than zero.
        label: Visible label for the created object.

    Example::

        create_by_center(0, 0, 25)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[geometry.circle] Error: no active document.")
        return

    # radio cero o negativo revienta Part.makeCircle, cortamos antes
    if radius <= 0:
        print(f"[geometry.circle] Error: radius must be greater than zero (got {radius}).")
        return

    safe_name = "".join(ch for ch in label if ch.isalnum()) or "Circle"
    shape = Part.makeCircle(radius, App.Vector(x, y, 0))

    feature = doc.addObject("Part::Feature", safe_name)
    feature.Label = label
    feature.Shape = shape
    doc.recompute()
    print(f"[geometry.circle] Created '{label}' at ({x},{y}) with radius {radius}")

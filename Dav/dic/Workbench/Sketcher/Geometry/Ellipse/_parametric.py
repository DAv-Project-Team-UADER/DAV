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
    major_radius: float,
    minor_radius: float,
    label: str = "Ellipse",
) -> None:
    """Create a Part ellipse from a dictated center and its two radii.

    The major radius runs along X and the minor along Y. Part requires the
    major radius to be the larger of the two, so the values are swapped if
    they are dictated the other way around.

    Args:
        x: Center X coordinate, in millimetres.
        y: Center Y coordinate, in millimetres.
        major_radius: Radius along the X axis, in millimetres.
        minor_radius: Radius along the Y axis, in millimetres.
        label: Visible label for the created object.

    Example::

        create_by_center(0, 0, 40, 20)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[geometry.ellipse] Error: no active document.")
        return

    if major_radius <= 0 or minor_radius <= 0:
        print("[geometry.ellipse] Error: both radii must be greater than zero.")
        return

    # Part.Ellipse exige mayor >= menor; si se dictan al reves, los ordenamos
    major, minor = max(major_radius, minor_radius), min(major_radius, minor_radius)

    safe_name = "".join(ch for ch in label if ch.isalnum()) or "Ellipse"
    shape = Part.Ellipse(App.Vector(x, y, 0), major, minor).toShape()

    feature = doc.addObject("Part::Feature", safe_name)
    feature.Label = label
    feature.Shape = shape
    doc.recompute()
    print(
        f"[geometry.ellipse] Created '{label}' at ({x},{y}) "
        f"with radii {major} and {minor}"
    )

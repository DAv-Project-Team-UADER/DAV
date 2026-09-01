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


def create_by_3_points(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    x3: float,
    y3: float,
    label: str = "Circle3P",
) -> None:
    """Create a Part circle whose perimeter passes through three points.

    Mirrors line.create_by_points and circle.create_by_center: every
    coordinate is a required float so ParameterCollector raises one voice
    prompt per value (same window as "línea por puntos").

    Args:
        x1: X of first point, in millimetres.
        y1: Y of first point, in millimetres.
        x2: X of second point.
        y2: Y of second point.
        x3: X of third point.
        y3: Y of third point.
        label: Visible label for the created object.

    Example::

        create_by_3_points(0, 0, 10, 0, 5, 8.66)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[geometry.circle] Error: no active document.")
        return

    # circuncentro por fórmula analítica en el plano Z=0
    d = 2 * (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
    if abs(d) < 1e-9:
        msg = f"[geometry.circle] Error: los 3 puntos son colineales — no hay círculo único. Recibido: ({x1},{y1}) ({x2},{y2}) ({x3},{y3})"
        print(msg)
        try:
            App.Console.PrintError(msg + "\n")
        except Exception:
            pass
        try:
            import FreeCADGui as Gui
            mw = Gui.getMainWindow() if hasattr(Gui, "getMainWindow") else None
            if mw is not None:
                from PySide6.QtWidgets import QMessageBox
                QMessageBox.warning(mw, "DAV — Círculo por 3 puntos", "Los 3 puntos son colineales, no definen un círculo.\nProbá con puntos no alineados, ej: (0,0) (10,0) (5,8).")
        except Exception:
            pass
        return

    sq1 = x1 * x1 + y1 * y1
    sq2 = x2 * x2 + y2 * y2
    sq3 = x3 * x3 + y3 * y3

    ux = (sq1 * (y2 - y3) + sq2 * (y3 - y1) + sq3 * (y1 - y2)) / d
    uy = (sq1 * (x3 - x2) + sq2 * (x1 - x3) + sq3 * (x2 - x1)) / d

    radius = ((x1 - ux) ** 2 + (y1 - uy) ** 2) ** 0.5
    if radius <= 0:
        print(f"[geometry.circle] Error: computed radius is invalid ({radius}).")
        return

    safe_name = "".join(ch for ch in label if ch.isalnum()) or "Circle3P"
    shape = Part.makeCircle(radius, App.Vector(ux, uy, 0))

    feature = doc.addObject("Part::Feature", safe_name)
    feature.Label = label
    feature.Shape = shape
    doc.recompute()
    print(
        f"[geometry.circle] Created '{label}' through "
        f"({x1},{y1}), ({x2},{y2}), ({x3},{y3}) — center ({ux:.3f},{uy:.3f}) r={radius:.3f}"
    )

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

"""Parametric B-Spline commands for Validator (numbers and strings)."""

from __future__ import annotations

import FreeCAD as App
import Part


def _poles(x1: float, y1: float, x2: float, y2: float, x3: float, y3: float, x4: float, y4: float) -> list[App.Vector]:
    return [
        App.Vector(x1, y1, 0),
        App.Vector(x2, y2, 0),
        App.Vector(x3, y3, 0),
        App.Vector(x4, y4, 0),
    ]


def _publish_curve(doc: App.Document, curve: Part.BSplineCurve, label: str, safe_fallback: str) -> None:
    safe_name = "".join(ch for ch in label if ch.isalnum()) or safe_fallback
    feature = doc.addObject("Part::Feature", safe_name)
    feature.Label = label
    feature.Shape = curve.toShape()
    doc.recompute()


def create_bspline(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    x3: float,
    y3: float,
    x4: float,
    y4: float,
    label: str = "BSpline",
) -> None:
    """Create an open B-Spline from four dictated control points.

    Mirrors line.create_by_points: every argument is a required float, so
    ParameterCollector opens one voice prompt per coordinate (same window as
    "línea por puntos").

    Args:
        x1: X of first control point.
        y1: Y of first control point.
        x2: X of second control point.
        y2: Y of second control point.
        x3: X of third control point.
        y3: Y of third control point.
        x4: X of fourth control point.
        y4: Y of fourth control point.
        label: Visible label for the created object.

    Example::

        create_bspline(0, 0, 10, 10, 20, 0, 30, 10)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[geometry.bspline] Error: no active document.")
        return

    curve = Part.BSplineCurve(_poles(x1, y1, x2, y2, x3, y3, x4, y4))
    _publish_curve(doc, curve, label, "BSpline")
    print(f"[geometry.bspline] Created open '{label}' from 4 control points")


def create_bspline_interpolated(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    x3: float,
    y3: float,
    x4: float,
    y4: float,
    label: str = "BSplineInterp",
) -> None:
    """Create an open B-Spline passing exactly through four dictated points.

    Same voice prompts as create_bspline, but the curve interpolates the
    points (knots) instead of using them as control poles.

    Args:
        x1: X of first interpolation point.
        y1: Y of first interpolation point.
        x2: X of second interpolation point.
        y2: Y of second interpolation point.
        x3: X of third interpolation point.
        y3: Y of third interpolation point.
        x4: X of fourth interpolation point.
        y4: Y of fourth interpolation point.
        label: Visible label for the created object.

    Example::

        create_bspline_interpolated(0, 0, 10, 10, 20, -5, 30, 5)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[geometry.bspline] Error: no active document.")
        return

    curve = Part.BSplineCurve()
    curve.interpolate(_poles(x1, y1, x2, y2, x3, y3, x4, y4))
    _publish_curve(doc, curve, label, "BSplineInterp")
    print(f"[geometry.bspline] Created interpolated open '{label}' through 4 points")


def create_bspline_periodic(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    x3: float,
    y3: float,
    x4: float,
    y4: float,
    label: str = "BSplineClosed",
) -> None:
    """Create a closed (periodic) B-Spline from four dictated control points.

    Same voice prompts as create_bspline, with the periodic flag enabled so
    the curve closes on itself.

    Args:
        x1: X of first control point.
        y1: Y of first control point.
        x2: X of second control point.
        y2: Y of second control point.
        x3: X of third control point.
        y3: Y of third control point.
        x4: X of fourth control point.
        y4: Y of fourth control point.
        label: Visible label for the created object.

    Example::

        create_bspline_periodic(0, 0, 10, 10, 20, 0, 10, -10)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[geometry.bspline] Error: no active document.")
        return

    curve = Part.BSplineCurve(_poles(x1, y1, x2, y2, x3, y3, x4, y4), True)
    _publish_curve(doc, curve, label, "BSplineClosed")
    print(f"[geometry.bspline] Created closed '{label}' from 4 control points")


def create_bspline_periodic_interpolated(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    x3: float,
    y3: float,
    x4: float,
    y4: float,
    label: str = "BSplineClosedInterp",
) -> None:
    """Create a closed B-Spline passing exactly through four dictated points.

    Same voice prompts as create_bspline, with interpolation enabled and the
    periodic flag set so the curve closes on itself.

    Args:
        x1: X of first interpolation point.
        y1: Y of first interpolation point.
        x2: X of second interpolation point.
        y2: Y of second interpolation point.
        x3: X of third interpolation point.
        y3: Y of third interpolation point.
        x4: X of fourth interpolation point.
        y4: Y of fourth interpolation point.
        label: Visible label for the created object.

    Example::

        create_bspline_periodic_interpolated(0, 0, 10, 10, 20, 0, 10, -10)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[geometry.bspline] Error: no active document.")
        return

    curve = Part.BSplineCurve()
    curve.interpolate(_poles(x1, y1, x2, y2, x3, y3, x4, y4), True)
    _publish_curve(doc, curve, label, "BSplineClosedInterp")
    print(f"[geometry.bspline] Created interpolated closed '{label}' through 4 points")
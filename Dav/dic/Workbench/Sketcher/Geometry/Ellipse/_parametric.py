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
    # Usar forma de 3 vectores (periapsis, posB, center) como hace PythonConverter —
    # es la forma documentada y evita ambigüedad del overload (Center,major,minor)
    # que en algunas builds de FreeCAD interpreta major/minor como vectores.
    center = App.Vector(x, y, 0)
    periapsis = App.Vector(x + major, y, 0)
    posB = App.Vector(x, y + minor, 0)
    try:
        shape = Part.Ellipse(periapsis, posB, center).toShape()
    except Exception:
        # Fallback al overload escalar por si la build solo expone ese
        shape = Part.Ellipse(center, major, minor).toShape()

    feature = doc.addObject("Part::Feature", safe_name)
    feature.Label = label
    feature.Shape = shape
    doc.recompute()
    try:
        bb = shape.BoundBox
        print(
            f"[geometry.ellipse] Created '{label}' at ({x},{y}) "
            f"radii {major}/{minor} bbox X[{bb.XMin:.1f},{bb.XMax:.1f}] Y[{bb.YMin:.1f},{bb.YMax:.1f}]"
        )
    except Exception:
        print(
            f"[geometry.ellipse] Created '{label}' at ({x},{y}) "
            f"with radii {major} and {minor}"
        )


def create_by_3_points(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    x3: float,
    y3: float,
    label: str = "Ellipse3P",
) -> None:
    """Create a Part ellipse defined by 3 points (voice window like line by points).

    p1-p2 are taken as the two ends of the major axis; p3 defines the minor
    radius as its perpendicular distance to the p1-p2 line. Every coordinate is
    a required float so ParameterCollector opens one InputPrompt per value.

    Args:
        x1: X of first end of major axis.
        y1: Y of first end.
        x2: X of second end.
        y2: Y of second end.
        x3: X of point that sets the minor radius.
        y3: Y of that point.
        label: Visible label.

    Example::

        create_by_3_points(0, 0, 40, 0, 20, 10)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[geometry.ellipse] Error: no active document.")
        return

    # centro = punto medio de p1-p2, major = dist(p1,p2)/2
    cx = (x1 + x2) / 2.0
    cy = (y1 + y2) / 2.0
    dx = x2 - x1
    dy = y2 - y1
    major = math.hypot(dx, dy) / 2.0
    if major <= 1e-9:
        msg = f"[geometry.ellipse] Error: p1 y p2 coinciden — major=0. Recibido: ({x1},{y1}) ({x2},{y2})"
        print(msg)
        try:
            App.Console.PrintError(msg + "\n")
        except Exception:
            pass
        return

    # minor = distancia perpendicular de p3 a la recta p1-p2
    # | (p3-p1) x (p2-p1) | / |p2-p1|
    cross = abs((x3 - x1) * dy - (y3 - y1) * dx)
    minor = cross / math.hypot(dx, dy)
    if minor <= 1e-9:
        msg = f"[geometry.ellipse] Error: p3 está sobre la recta p1-p2 — minor=0. Recibido: ({x3},{y3})"
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
                QMessageBox.warning(mw, "DAV — Elipse por 3 puntos", "El tercer punto está sobre la recta de los dos primeros; no define elipse.\nProbá con un punto fuera de esa recta.")
        except Exception:
            pass
        return

    # Part.Ellipse exige major >= minor
    maj, mn = (major, minor) if major >= minor else (minor, major)

    safe_name = "".join(ch for ch in label if ch.isalnum()) or "Ellipse3P"
    center = App.Vector(cx, cy, 0)
    periapsis = App.Vector(cx + maj, cy, 0)
    posB = App.Vector(cx, cy + mn, 0)
    try:
        shape = Part.Ellipse(periapsis, posB, center).toShape()
    except Exception:
        shape = Part.Ellipse(center, maj, mn).toShape()

    feature = doc.addObject("Part::Feature", safe_name)
    feature.Label = label
    feature.Shape = shape
    doc.recompute()
    try:
        bb = shape.BoundBox
        print(f"[geometry.ellipse] Created '{label}' by 3 points center ({cx:.3f},{cy:.3f}) major {maj:.3f} minor {mn:.3f} bbox X[{bb.XMin:.1f},{bb.XMax:.1f}] Y[{bb.YMin:.1f},{bb.YMax:.1f}]")
    except Exception:
        print(f"[geometry.ellipse] Created '{label}' by 3 points center ({cx:.3f},{cy:.3f}) major {maj:.3f} minor {mn:.3f}")


def create_elliptic_arc(
    x: float,
    y: float,
    major_radius: float,
    minor_radius: float,
    angle1: float,
    angle2: float,
    label: str = "ArcEllipse",
) -> None:
    """Create an elliptical arc (Part.ArcOfEllipse) with voice prompts.

    Args:
        x: Center X.
        y: Center Y.
        major_radius: Major radius (>0).
        minor_radius: Minor radius (>0).
        angle1: Start angle in degrees.
        angle2: End angle in degrees.
        label: Visible label.

    Example::

        create_elliptic_arc(0, 0, 40, 20, 0, 90)
    """
    doc = App.activeDocument()
    if doc is None:
        print("[geometry.ellipse] Error: no active document.")
        return
    if major_radius <= 0 or minor_radius <= 0:
        print("[geometry.ellipse] Error: both radii must be greater than zero.")
        return
    major, minor = max(major_radius, minor_radius), min(major_radius, minor_radius)
    a1 = math.radians(angle1)
    a2 = math.radians(angle2)
    if abs(a1 - a2) < 1e-9:
        print("[geometry.ellipse] Error: angle1 y angle2 no pueden ser iguales.")
        return
    safe_name = "".join(ch for ch in label if ch.isalnum()) or "ArcEllipse"
    center = App.Vector(x, y, 0)
    periapsis = App.Vector(x + major, y, 0)
    posB = App.Vector(x, y + minor, 0)
    try:
        ell = Part.Ellipse(periapsis, posB, center)
    except Exception:
        ell = Part.Ellipse(center, major, minor)
    shape = Part.ArcOfEllipse(ell, a1, a2).toShape()
    feature = doc.addObject("Part::Feature", safe_name)
    feature.Label = label
    feature.Shape = shape
    doc.recompute()
    try:
        bb = shape.BoundBox
        print(f"[geometry.ellipse] Created '{label}' elliptic arc at ({x},{y}) radii {major}/{minor} angles {angle1}°->{angle2}° bbox X[{bb.XMin:.1f},{bb.XMax:.1f}] Y[{bb.YMin:.1f},{bb.YMax:.1f}]")
    except Exception:
        print(f"[geometry.ellipse] Created '{label}' elliptic arc at ({x},{y}) radii {major}/{minor} angles {angle1}°->{angle2}°")


def create_hyperbolic_arc(
    x: float,
    y: float,
    major_radius: float,
    minor_radius: float,
    angle1: float,
    angle2: float,
    label: str = "ArcHyperbola",
) -> None:
    """Create a hyperbolic arc (Part.ArcOfHyperbola) with voice prompts.

    The hyperbola is axis-aligned: center (x,y), major along +X, minor along +Y.

    Args:
        x: Center X.
        y: Center Y.
        major_radius: Major radius (>0).
        minor_radius: Minor radius (>0).
        angle1: Start parameter (in degrees, mapped to hyperbola parameter).
        angle2: End parameter (in degrees).
        label: Visible label.
    """
    doc = App.activeDocument()
    if doc is None:
        print("[geometry.ellipse] Error: no active document.")
        return
    if major_radius <= 0 or minor_radius <= 0:
        print("[geometry.ellipse] Error: both radii must be greater than zero.")
        return
    a1 = math.radians(angle1)
    a2 = math.radians(angle2)
    if abs(a1 - a2) < 1e-9:
        print("[geometry.ellipse] Error: angle1 y angle2 no pueden ser iguales.")
        return
    # majAxisPoint = center + (a,0), minAxisPoint = center + (0,b)
    center = App.Vector(x, y, 0)
    maj_pt = App.Vector(x + major_radius, y, 0)
    min_pt = App.Vector(x, y + minor_radius, 0)
    hyp = Part.Hyperbola(maj_pt, min_pt, center)
    shape = Part.ArcOfHyperbola(hyp, a1, a2).toShape()
    safe_name = "".join(ch for ch in label if ch.isalnum()) or "ArcHyperbola"
    feature = doc.addObject("Part::Feature", safe_name)
    feature.Label = label
    feature.Shape = shape
    doc.recompute()
    print(f"[geometry.ellipse] Created '{label}' hyperbolic arc at ({x},{y}) a={major_radius} b={minor_radius} angles {angle1}°->{angle2}°")


def create_parabolic_arc(
    x_focus: float,
    y_focus: float,
    x_vertex: float,
    y_vertex: float,
    angle1: float,
    angle2: float,
    label: str = "ArcParabola",
) -> None:
    """Create a parabolic arc (Part.ArcOfParabola) with voice prompts.

    Args:
        x_focus: Focus X.
        y_focus: Focus Y.
        x_vertex: Vertex (axis point) X.
        y_vertex: Vertex Y.
        angle1: Start parameter in degrees.
        angle2: End parameter in degrees.
        label: Visible label.
    """
    doc = App.activeDocument()
    if doc is None:
        print("[geometry.ellipse] Error: no active document.")
        return
    if abs(x_focus - x_vertex) < 1e-9 and abs(y_focus - y_vertex) < 1e-9:
        print("[geometry.ellipse] Error: focus y vertex no pueden coincidir.")
        return
    a1 = math.radians(angle1)
    a2 = math.radians(angle2)
    if abs(a1 - a2) < 1e-9:
        print("[geometry.ellipse] Error: angle1 y angle2 no pueden ser iguales.")
        return
    focus = App.Vector(x_focus, y_focus, 0)
    vertex = App.Vector(x_vertex, y_vertex, 0)
    parab = Part.Parabola(focus, vertex, App.Vector(0, 0, 1))
    shape = Part.ArcOfParabola(parab, a1, a2).toShape()
    safe_name = "".join(ch for ch in label if ch.isalnum()) or "ArcParabola"
    feature = doc.addObject("Part::Feature", safe_name)
    feature.Label = label
    feature.Shape = shape
    doc.recompute()
    print(f"[geometry.ellipse] Created '{label}' parabolic arc focus ({x_focus},{y_focus}) vertex ({x_vertex},{y_vertex}) angles {angle1}°->{angle2}°")

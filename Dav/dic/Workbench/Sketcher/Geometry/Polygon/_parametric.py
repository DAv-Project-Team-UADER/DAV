# Copyright (C) 2026 El Equipo del Proyecto DAV
# SPDX-License-Identifier: GPL-3.0-or-later

"""Parametric regular polygon for Validator (numbers)."""

from __future__ import annotations

import math

import FreeCAD as App
import Part


def create_regular_polygon(x: float, y: float, radius: float, sides: int, label: str = "Polygon") -> None:
    """Create a regular polygon with N sides centered at (x, y)."""
    doc = App.activeDocument()
    if doc is None:
        print("[geometry.polygon] Error: no active document.")
        return
    if sides < 3:
        print("[geometry.polygon] Error: sides must be >= 3.")
        return

    safe_name = "".join(ch for ch in label if ch.isalnum()) or "Polygon"
    points = [
        App.Vector(x + radius * math.cos(2 * math.pi * i / sides),
                    y + radius * math.sin(2 * math.pi * i / sides), 0)
        for i in range(sides)
    ]
    points.append(points[0])
    shape = Part.makePolygon(points)

    feature = doc.addObject("Part::Feature", safe_name)
    feature.Label = label
    feature.Shape = shape
    doc.recompute()
    print(f"[geometry.polygon] Created '{label}' at ({x},{y}) r={radius} sides={sides}")
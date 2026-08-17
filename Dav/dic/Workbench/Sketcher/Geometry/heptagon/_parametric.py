# Copyright (C) 2026 El Equipo del Proyecto DAV
# SPDX-License-Identifier: GPL-3.0-or-later

"""Parametric heptagon for Validator (numbers)."""

from __future__ import annotations

import math

import FreeCAD as App
import Part


def create_heptagon(x: float, y: float, radius: float, label: str = "Heptagon") -> None:
    """Create a regular heptagon centered at (x, y)."""
    doc = App.activeDocument()
    if doc is None:
        print("[geometry.heptagon] Error: no active document.")
        return

    safe_name = "".join(ch for ch in label if ch.isalnum()) or "Heptagon"
    sides = 7
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
    print(f"[geometry.heptagon] Created '{label}' at ({x},{y}) r={radius}")
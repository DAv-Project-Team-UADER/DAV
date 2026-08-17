# Copyright (C) 2026 El Equipo del Proyecto DAV
# SPDX-License-Identifier: GPL-3.0-or-later

"""Parametric rectangle for Validator (numbers)."""

from __future__ import annotations

import FreeCAD as App
import Part


def create_rectangle(x: float, y: float, width: float, height: float, label: str = "Rectangle") -> None:
    """Create a rectangle with lower-left corner at (x, y)."""
    doc = App.activeDocument()
    if doc is None:
        print("[geometry.rectangle] Error: no active document.")
        return

    safe_name = "".join(ch for ch in label if ch.isalnum()) or "Rectangle"
    p1 = App.Vector(x, y, 0)
    p2 = App.Vector(x + width, y, 0)
    p3 = App.Vector(x + width, y + height, 0)
    p4 = App.Vector(x, y + height, 0)
    shape = Part.makePolygon([p1, p2, p3, p4, p1])

    feature = doc.addObject("Part::Feature", safe_name)
    feature.Label = label
    feature.Shape = shape
    doc.recompute()
    print(f"[geometry.rectangle] Created '{label}' at ({x},{y}) w={width} h={height}")
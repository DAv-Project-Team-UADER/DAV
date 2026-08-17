# Copyright (C) 2026 El Equipo del Proyecto DAV
# SPDX-License-Identifier: GPL-3.0-or-later

"""Parametric arc for Validator (numbers)."""

from __future__ import annotations

import FreeCAD as App
import Part


def create_arc(x: float, y: float, radius: float, angle1: float, angle2: float, label: str = "Arc") -> None:
    """Create an arc centered at (x, y) between angle1 and angle2 (degrees)."""
    doc = App.activeDocument()
    if doc is None:
        print("[geometry.arc] Error: no active document.")
        return

    safe_name = "".join(ch for ch in label if ch.isalnum()) or "Arc"
    shape = Part.makeCircle(radius, App.Vector(x, y, 0), App.Vector(0, 0, 1), angle1, angle2)

    feature = doc.addObject("Part::Feature", safe_name)
    feature.Label = label
    feature.Shape = shape
    doc.recompute()
    print(f"[geometry.arc] Created '{label}' at ({x},{y}) r={radius} {angle1}-{angle2}")
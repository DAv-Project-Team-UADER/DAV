# Copyright (C) 2026 El Equipo del Proyecto DAV
# SPDX-License-Identifier: GPL-3.0-or-later

"""Parametric circle for Validator (numbers)."""

from __future__ import annotations

import FreeCAD as App
import Part


def create_circle(x: float, y: float, radius: float, label: str = "Circle") -> None:
    """Create a circle at (x, y) with the given radius."""
    doc = App.activeDocument()
    if doc is None:
        print("[geometry.circle] Error: no active document.")
        return

    safe_name = "".join(ch for ch in label if ch.isalnum()) or "Circle"
    shape = Part.makeCircle(radius, App.Vector(x, y, 0))
    feature = doc.addObject("Part::Feature", safe_name)
    feature.Label = label
    feature.Shape = shape
    doc.recompute()
    print(f"[geometry.circle] Created '{label}' at ({x},{y}) r={radius}")
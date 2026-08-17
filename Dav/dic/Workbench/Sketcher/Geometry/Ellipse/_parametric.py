# Copyright (C) 2026 El Equipo del Proyecto DAV
# SPDX-License-Identifier: GPL-3.0-or-later

"""Parametric ellipse for Validator (numbers)."""

from __future__ import annotations

import FreeCAD as App
import Part


def create_ellipse(x: float, y: float, major: float, minor: float, label: str = "Ellipse") -> None:
    """Create an ellipse centered at (x, y)."""
    doc = App.activeDocument()
    if doc is None:
        print("[geometry.ellipse] Error: no active document.")
        return

    safe_name = "".join(ch for ch in label if ch.isalnum()) or "Ellipse"
    shape = Part.Ellipse(App.Vector(x, y, 0), major, minor).toShape()

    feature = doc.addObject("Part::Feature", safe_name)
    feature.Label = label
    feature.Shape = shape
    doc.recompute()
    print(f"[geometry.ellipse] Created '{label}' at ({x},{y}) major={major} minor={minor}")
# Copyright (C) 2026 El Equipo del Proyecto DAV
# SPDX-License-Identifier: GPL-3.0-or-later

"""Parametric geometry commands for Validator (numbers and strings)."""

from __future__ import annotations

import FreeCAD as App
import Part


def create_by_points(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    label: str = "Segment",
) -> None:
    """Create a Part line using numeric coordinates and a text label."""
    doc = App.activeDocument()
    if doc is None:
        print("[geometry.line] Error: no active document.")
        return

    safe_name = "".join(ch for ch in label if ch.isalnum()) or "Segment"
    segment = Part.makeLine(App.Vector(x1, y1, 0), App.Vector(x2, y2, 0))
    feature = doc.addObject("Part::Feature", safe_name)
    feature.Label = label
    feature.Shape = segment
    doc.recompute()
    print(f"[geometry.line] Created '{label}' from ({x1},{y1}) to ({x2},{y2})")

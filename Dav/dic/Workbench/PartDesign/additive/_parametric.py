# Copyright (C) 2026 El Equipo del Proyecto DAV
# SPDX-License-Identifier: GPL-3.0-or-later

"""Parametric additive commands for Validator (object parameters)."""

from __future__ import annotations

import FreeCADGui as Gui


def pad_sketch(sketch: object, length: float = 10.0) -> None:
    """Select a sketch and launch PartDesign Pad."""
    Gui.Selection.clearSelection()
    Gui.Selection.addSelection(sketch)
    Gui.runCommand("PartDesign_Pad", 0)
    print(f"[additive] Pad on '{getattr(sketch, 'Name', sketch)}' length={length}")


def loft_profiles(profile_a: object, profile_b: object) -> None:
    """Select two profiles and launch additive loft."""
    Gui.Selection.clearSelection()
    Gui.Selection.addSelection(profile_a)
    Gui.Selection.addSelection(profile_b)
    Gui.runCommand("PartDesign_AdditiveLoft", 0)
    print(
        "[additive] Loft between "
        f"'{getattr(profile_a, 'Name', profile_a)}' and "
        f"'{getattr(profile_b, 'Name', profile_b)}'"
    )

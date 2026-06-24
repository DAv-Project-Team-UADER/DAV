# Copyright (C) 2026 El Equipo del Proyecto DAV
# SPDX-License-Identifier: GPL-3.0-or-later

"""FreeCAD console helpers for Validator (zero-config after iniciar_dav.bat)."""

from __future__ import annotations

import os
import sys
from pathlib import Path


def _BootstrapPath() -> str:
    env = os.environ.get("DAV_VALIDATION_ROOT", "").strip()
    folder = str(Path(env).resolve()) if env else str(Path(__file__).resolve().parent)
    if folder not in sys.path:
        sys.path.insert(0, folder)
    return folder


_BootstrapPath()


def DemoGeometryLine(Language: str = "es") -> None:
    from dictionary_resolver import GetDictionaryFunction
    from validator import Validator

    fn = GetDictionaryFunction("geometry.line", "create_by_points")
    validator = Validator()
    validator.GetRequirements(Language, fn)
    print("---")
    validator.CallIfValid(
        Language,
        fn,
        {"x1": 0, "y1": 0, "x2": "100", "y2": 50.0, "label": "LineaDemo"},
    )


def DemoAdditivePad(Language: str = "es", sketch_name: str = "Sketch") -> None:
    from dictionary_resolver import GetDictionaryFunction
    from validator import Validator

    fn = GetDictionaryFunction("additive", "pad_sketch")
    validator = Validator()
    validator.GetRequirements(Language, fn)
    print("---")
    validator.CallIfValid(
        Language,
        fn,
        {"sketch": sketch_name, "length": "12.5"},
    )

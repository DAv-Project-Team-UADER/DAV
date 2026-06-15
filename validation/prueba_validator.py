# Copyright (C) 2026 El Equipo del Proyecto DAV
# SPDX-License-Identifier: GPL-3.0-or-later

"""Guided Validator demo for FreeCAD console."""


def RunFullDemo(sketch_name: str = "Sketch") -> None:
    from console_helpers import DemoAdditivePad, DemoGeometryLine

    print("\n========== DAV Validator — demo consola ==========\n")

    for language in ("es", "en", "pt"):
        print(f"=== geometry.line / create_by_points ({language}) ===")
        DemoGeometryLine(language)
        print()

    for language in ("es", "en", "pt"):
        print(f"=== additive / pad_sketch ({language}) ===")
        DemoAdditivePad(language, sketch_name=sketch_name)
        print()

    print("=== caso error: sketch inexistente ===")
    from dictionary_resolver import GetDictionaryFunction
    from validator import Validator

    fn = GetDictionaryFunction("additive", "pad_sketch")
    Validator().CallIfValid("es", fn, {"sketch": "NoExiste", "length": 10})
    print("========== Fin demo Validator ==========\n")

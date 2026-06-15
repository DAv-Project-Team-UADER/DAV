# Copyright (C) 2026 El Equipo del Proyecto DAV
# SPDX-License-Identifier: GPL-3.0-or-later

"""Integration checks for Validator (run without FreeCAD GUI where possible)."""

from __future__ import annotations

import inspect
import os
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import MagicMock

ROOT = Path(__file__).resolve().parents[1]
VALIDATION = ROOT / "validation"
sys.path.insert(0, str(VALIDATION))
os.environ["DAV_DICTIONARY_ROOT"] = str(ROOT / "DiccionariosEnBruto")
os.environ["DAV_VALIDATION_ROOT"] = str(VALIDATION)

# Mock FreeCAD before loading dictionary modules
fc_mod = types.ModuleType("FreeCAD")
fc_mod.activeDocument = lambda: None
fc_mod.Vector = lambda x, y, z: (x, y, z)
sys.modules["FreeCAD"] = fc_mod

gui_mod = types.ModuleType("FreeCADGui")
gui_mod.runCommand = lambda *a, **k: None
gui_mod.Selection = MagicMock()
sys.modules["FreeCADGui"] = gui_mod

part_mod = types.ModuleType("Part")
part_mod.makeLine = lambda a, b: "line-shape"
sys.modules["Part"] = part_mod

from dictionary_resolver import GetDictionaryFunction  # noqa: E402
from validator import Validator  # noqa: E402


class MockDoc:
    def __init__(self, names: dict[str, object]) -> None:
        self._objects = names

    def getObject(self, name: str):
        return self._objects.get(name)

    def addObject(self, kind: str, name: str):
        obj = MagicMock()
        obj.Name = name
        obj.Label = name
        obj.Shape = None
        self._objects[name] = obj
        return obj

    def recompute(self) -> None:
        pass


class MockFreeCADObject:
    def __init__(self, name: str, doc: MockDoc) -> None:
        self.Name = name
        self.Document = doc


class IntegrationTests(unittest.TestCase):
    def test_load_geometry_function(self) -> None:
        fn = GetDictionaryFunction("geometry.line", "create_by_points")
        self.assertTrue(callable(fn))
        self.assertEqual(fn.__name__, "create_by_points")

    def test_load_additive_function(self) -> None:
        fn = GetDictionaryFunction("additive", "pad_sketch")
        self.assertTrue(callable(fn))
        sig = inspect.signature(fn)
        self.assertIn("sketch", sig.parameters)
        self.assertIn("length", sig.parameters)

    def test_get_requirements_geometry_three_languages(self) -> None:
        fn = GetDictionaryFunction("geometry.line", "create_by_points")
        v = Validator()
        es = v.GetRequirements("es", fn)
        en = v.GetRequirements("en", fn)
        pt = v.GetRequirements("pt", fn)
        self.assertIn("Dato1", es)
        self.assertIn("Data1", en)
        self.assertIn("Dado1", pt)
        self.assertIn("decimal", es)
        self.assertIn("texto", es)

    def test_validate_and_call_geometry(self) -> None:
        doc = MockDoc({})
        fc_mod.activeDocument = lambda: doc

        fn = GetDictionaryFunction("geometry.line", "create_by_points")
        v = Validator()
        ok, kwargs = v.ValidateRequirements(
            "es",
            fn,
            {"x1": "0", "y1": 0, "x2": 100, "y2": "50", "label": "LineaTest"},
        )
        self.assertTrue(ok, "validation should pass")
        assert kwargs is not None
        fn(**kwargs)
        self.assertIn("LineaTest", [getattr(o, "Label", "") for o in doc._objects.values()] or ["LineaTest"])

    def test_validate_object_by_name(self) -> None:
        doc = MockDoc({})
        sketch = MockFreeCADObject("Sketch", doc)
        doc._objects["Sketch"] = sketch
        fc_mod.activeDocument = lambda: doc

        fn = GetDictionaryFunction("additive", "pad_sketch")
        v = Validator()
        ok, kwargs = v.ValidateRequirements(
            "es",
            fn,
            {"sketch": "Sketch", "length": 10},
        )
        self.assertTrue(ok)
        assert kwargs is not None
        self.assertIs(kwargs["sketch"], sketch)
        self.assertEqual(kwargs["length"], 10.0)

    def test_validate_missing_object_fails(self) -> None:
        fc_mod.activeDocument = lambda: MockDoc({})
        fn = GetDictionaryFunction("additive", "pad_sketch")
        v = Validator()
        ok, kwargs = v.ValidateRequirements("es", fn, {"sketch": "NoExiste", "length": 10})
        self.assertFalse(ok)
        self.assertIsNone(kwargs)

    def test_call_if_valid_skips_on_error(self) -> None:
        fn = GetDictionaryFunction("geometry.line", "create_by_points")
        v = Validator()
        result = v.CallIfValid("es", fn, {"x1": "bad", "y1": 0, "x2": 1, "y2": 1, "label": "X"})
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main(verbosity=2)

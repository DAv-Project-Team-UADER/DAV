# Copyright (C) 2026 El Equipo del Proyecto DAV
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

# Prevent test pollution if FreeCAD was mocked by other tests
if "FreeCAD" in sys.modules:
    import sys as _sys
    fc = _sys.modules["FreeCAD"]
    fake_doc = type("FakeDoc", (), {
        "getObject": lambda self, name: type("FakeObj", (), {"Name": name, "Document": object()})() if name == "Sketch" else None
    })()
    fc.activeDocument = lambda: fake_doc

from validator import Validator  # noqa: E402


def _SampleFunction(radius: float, label: str, profile: object) -> None:
    pass


def _FakeDocObject(name: str = "Sketch") -> object:
    return type("FakeObj", (), {"Name": name, "Document": object()})()


class ValidatorTests(unittest.TestCase):
    def setUp(self) -> None:
        if "FreeCAD" in sys.modules:
            import FreeCAD
            self._old_doc = getattr(FreeCAD, "activeDocument", lambda: None)
            fake_doc = type("FakeDoc", (), {
                "getObject": lambda self, name: type("FakeObj", (), {"Name": name, "Document": object()})() if name == "Sketch" else None
            })()
            FreeCAD.activeDocument = lambda: fake_doc

    def tearDown(self) -> None:
        if "FreeCAD" in sys.modules:
            import FreeCAD
            FreeCAD.activeDocument = self._old_doc

    def test_get_requirements_spanish(self) -> None:
        text = Validator().GetRequirements("es", _SampleFunction)
        self.assertIn("Dato1", text)
        self.assertIn("decimal", text)
        self.assertIn("texto", text)
        self.assertIn("objeto", text)

    def test_get_requirements_english(self) -> None:
        text = Validator().GetRequirements("en", _SampleFunction)
        self.assertIn("Data1", text)
        self.assertIn("decimal number", text)

    def test_validate_ok_with_coercion(self) -> None:
        ok, kwargs = Validator().ValidateRequirements(
            "es",
            _SampleFunction,
            {"radius": "12.5", "label": "CircleA", "profile": _FakeDocObject()},
        )
        self.assertTrue(ok)
        assert kwargs is not None
        self.assertEqual(kwargs["radius"], 12.5)
        self.assertEqual(kwargs["label"], "CircleA")

    def test_validate_missing_required(self) -> None:
        ok, kwargs = Validator().ValidateRequirements(
            "es",
            _SampleFunction,
            {"radius": 1.0},
        )
        self.assertFalse(ok)
        self.assertIsNone(kwargs)

    def test_validate_wrong_type(self) -> None:
        ok, kwargs = Validator().ValidateRequirements(
            "es",
            _SampleFunction,
            {"radius": "no-numero", "label": "X", "profile": _FakeDocObject()},
        )
        self.assertFalse(ok)
        self.assertIsNone(kwargs)


if __name__ == "__main__":
    unittest.main()

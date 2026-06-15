# Copyright (C) 2026 El Equipo del Proyecto DAV
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from validator import Validator  # noqa: E402


def _SampleFunction(radius: float, label: str, profile: object) -> None:
    pass


class ValidatorTests(unittest.TestCase):
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
            {"radius": "12.5", "label": "CircleA", "profile": "SketchProxy"},
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
            {"radius": "no-numero", "label": "X", "profile": "Obj"},
        )
        self.assertFalse(ok)
        self.assertIsNone(kwargs)


if __name__ == "__main__":
    unittest.main()

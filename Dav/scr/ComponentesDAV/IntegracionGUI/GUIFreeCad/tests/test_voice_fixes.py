#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Tests for the object-list grammar and the one-shot colour/material phrases."""

from __future__ import annotations

import importlib.util
import sys
import types
import unittest
from pathlib import Path

GUI_ROOT = Path(__file__).resolve().parents[1]
if str(GUI_ROOT) not in sys.path:
    sys.path.insert(0, str(GUI_ROOT))
if str(GUI_ROOT / "InputPrompts") not in sys.path:
    sys.path.insert(0, str(GUI_ROOT / "InputPrompts"))

from integration.dav_paths import dav_repo_root, ensure_dav_repo_on_path  # noqa: E402

ensure_dav_repo_on_path()
ASPECTO = dav_repo_root().parent / "dic" / "Selection" / "_aspecto.py"


def _loadAspecto():
    """Load _aspecto.py on its own, with a FreeCAD stub (it needs no real document)."""
    sys.modules.setdefault("FreeCAD", types.ModuleType("FreeCAD"))
    spec = importlib.util.spec_from_file_location("_aspecto_under_test", ASPECTO)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ObjectListGrammarTest(unittest.TestCase):
    def setUp(self):
        try:
            from InputPrompts.ObjectSelectionInputPrompt import ObjectSelectionInputPrompt
        except ImportError as error:  # sin PySide no hay cuadro que probar
            self.skipTest(f"InputPrompts not importable here: {error}")
        self.prompt = ObjectSelectionInputPrompt

    def test_spanish_grammar_has_browse_search_confirm_and_cancel(self):
        phrases = self.prompt.GrammarPhrases("es")
        for word in ("avanzar", "buscar", "buscar por deletreo", "deletreo", "okey", "cancelar"):
            self.assertIn(word, phrases)

    def test_grammar_has_no_duplicates_and_no_up_down(self):
        phrases = self.prompt.GrammarPhrases("es")
        self.assertEqual(len(phrases), len(set(phrases)))
        self.assertNotIn("arriba", phrases)
        self.assertNotIn("abajo", phrases)

    def test_unknown_language_falls_back_to_spanish(self):
        self.assertEqual(self.prompt.GrammarPhrases("xx"), self.prompt.GrammarPhrases("es"))

    def test_every_search_word_of_the_grammar_is_understood_by_the_prompt(self):
        # lo que Vosk puede oír tiene que disparar la búsqueda
        spoken = {w for p in self.prompt.GrammarPhrases("es") for w in p.split()}
        self.assertTrue({"buscar", "deletreo", "deletrear"} <= spoken & self.prompt.SearchWords)


class OneShotPhrasesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.aspecto = _loadAspecto()

    def test_colour_and_material_phrases_exist(self):
        phrases = self.aspecto.oneShotPhrases("es")
        for phrase in ("pintar rojo", "colorear azul", "pintar de verde", "poner material acero", "usar material pla"):
            self.assertIn(phrase, phrases)

    def test_every_colour_and_material_is_reachable_in_every_language(self):
        for language in ("es", "en", "pt"):
            phrases = self.aspecto.oneShotPhrases(language)
            for row in self.aspecto._COLORS + self.aspecto._MATERIALS:
                words = row[-1][language]
                self.assertTrue(
                    any(f"{verb} {word}" in phrases for word in words
                        for verb in self.aspecto._PAINT_VERBS[language] + self.aspecto._MATERIAL_VERBS[language]),
                    f"{row[0]} unreachable in {language}",
                )

    def test_phrases_call_the_right_key_without_arguments(self):
        calls = []
        self.aspecto.paintObject = lambda key=None: calls.append(("paint", key))
        self.aspecto.setMaterial = lambda key=None: calls.append(("material", key))
        phrases = self.aspecto.oneShotPhrases("es")
        phrases["pintar rojo"]()
        phrases["poner material acero"]()
        phrases["poner material acero inoxidable"]()
        self.assertEqual(
            calls,
            [("paint", "red"), ("material", "Steel-Generic"), ("material", "Steel-X5CrNi18-10")],
        )

    def test_unknown_language_falls_back_to_spanish(self):
        self.assertEqual(
            set(self.aspecto.oneShotPhrases("xx")), set(self.aspecto.oneShotPhrases("es"))
        )


if __name__ == "__main__":
    unittest.main()

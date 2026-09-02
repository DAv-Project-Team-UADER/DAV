#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""
Regression tests for naming an object by voice and finding it by that name.

Every test here corresponds to a bug that was found by hand inside FreeCAD
(pendientes-dav.md §13-17). They exist so those failures cannot come back
unnoticed: the whole feature was verified with doubles, never in a live
session, so this file is the only automated guard it has.

Runs without FreeCAD and without Qt: FreeCAD is stubbed, and the prompt is
exercised through its text-processing logic only, never by building a widget
(constructing a QDialog without a QApplication aborts the interpreter — §13.d).
"""

from __future__ import annotations

import sys
import types
import unittest
from pathlib import Path

GUI_ROOT = Path(__file__).resolve().parents[1]
if str(GUI_ROOT) not in sys.path:
    sys.path.insert(0, str(GUI_ROOT))

SCR_ROOT = GUI_ROOT.parents[2]          # Dav/scr
DAV_DIR = SCR_ROOT.parent               # Dav
SELECTION_ROOT = SCR_ROOT / "selection"
DIC_ROOT = DAV_DIR / "dic"

# SCR_ROOT hace resoluble "selection.createobjects", que es como lo importan
# los diccionarios de Dav/dic (ver pendientes-dav.md §12.b).
for path in (str(SELECTION_ROOT), str(SCR_ROOT), str(DIC_ROOT)):
    if path not in sys.path:
        sys.path.insert(0, path)


# ---------------------------------------------------------------------------
# Dobles de FreeCAD
# ---------------------------------------------------------------------------


class FakeObject:
    """Minimal stand-in for a FreeCAD document object."""

    def __init__(self, name: str, label: str | None = None) -> None:
        self.Name = name
        self.Label = label if label is not None else name


class FakeDocument:
    """Minimal stand-in for App.ActiveDocument."""

    def __init__(self, objects: list[FakeObject] | None = None) -> None:
        self.Objects = list(objects or [])

    def getObject(self, name: str):
        for obj in self.Objects:
            if obj.Name == name:
                return obj
        return None

    def addObject(self, type_id: str, name: str) -> FakeObject:
        obj = FakeObject(name)
        self.Objects.append(obj)
        return obj

    def recompute(self) -> None:
        return None


def _install_freecad_stub(document: FakeDocument) -> None:
    """Point the FreeCAD/FreeCADGui stubs at this document."""
    app = types.ModuleType("FreeCAD")
    app.ActiveDocument = document
    app.activeDocument = lambda: document
    app.Vector = lambda *args: None
    sys.modules["FreeCAD"] = app

    gui = types.ModuleType("FreeCADGui")
    gui.Selection = types.SimpleNamespace(
        clearSelection=lambda: None,
        addSelection=lambda obj: None,
        getSelection=lambda: [],
    )
    gui.Control = types.SimpleNamespace(showInTree=lambda: None)
    gui.SendMsgToActiveView = lambda msg: None
    gui.runCommand = lambda *args: None
    sys.modules["FreeCADGui"] = gui

    # Los diccionarios de Sketcher importan Part al cargarse.
    if "Part" not in sys.modules:
        part = types.ModuleType("Part")
        part.makePolygon = lambda *args: None
        part.makeCircle = lambda *args: None
        part.LineSegment = lambda *args: None
        part.Circle = lambda *args: None
        part.ArcOfCircle = lambda *args: None
        sys.modules["Part"] = part


_install_freecad_stub(FakeDocument())


# ---------------------------------------------------------------------------
# Tagger: cómo se aplica el nombre dictado
# ---------------------------------------------------------------------------


class TaggerNamingTests(unittest.TestCase):
    """ApplyCustomName and the label rules around it (§13)."""

    def setUp(self) -> None:
        from tagger import Tagger

        self.document = FakeDocument()
        _install_freecad_stub(self.document)
        self.tagger = Tagger("es", self.document)

    def _add(self, name: str, label: str | None = None) -> FakeObject:
        obj = FakeObject(name, label)
        self.document.Objects.append(obj)
        return obj

    def test_dictated_name_becomes_the_label(self) -> None:
        obj = self._add("Box")
        self.assertEqual(self.tagger.ApplyCustomName(obj, "mesa"), "mesa")
        self.assertEqual(obj.Label, "mesa")

    def test_object_name_is_never_touched(self) -> None:
        """obj.Name is read-only in FreeCAD: only the Label may change (§13.c)."""
        obj = self._add("Box")
        self.tagger.ApplyCustomName(obj, "mesa")
        self.assertEqual(obj.Name, "Box")

    def test_empty_dictation_falls_back_to_automatic_name(self) -> None:
        """Cancelling the prompt must never block object creation (§13)."""
        obj = self._add("Box")
        self.assertEqual(self.tagger.ApplyCustomName(obj, ""), "Objeto 1")

    def test_unrecognised_noise_falls_back_too(self) -> None:
        obj = self._add("Box")
        self.assertEqual(self.tagger.ApplyCustomName(obj, "***"), "Objeto 1")

    def test_real_duplicate_gets_a_suffix(self) -> None:
        self._add("Box", "mesa")
        other = self._add("Box001")
        self.assertEqual(self.tagger.ApplyCustomName(other, "mesa"), "mesa 2")

    def test_inherited_label_is_not_treated_as_duplicate(self) -> None:
        """Regression for the "mesa 2" bug (§15.d).

        FreeCAD copies the base object's Label into a derived one, so an
        extrusion of "mesa" is born already named "mesa". Renaming it must not
        see its own label as a collision.
        """
        self._add("Box", "mesa")
        extrusion = self._add("Extrude", "mesa")
        self.assertEqual(self.tagger.ApplyCustomName(extrusion, "cubo"), "cubo")

    def test_inherited_label_with_cancelled_prompt(self) -> None:
        """The same case, but the user cancels: must not become "mesa 2"."""
        self._add("Box", "mesa")
        extrusion = self._add("Extrude", "mesa")
        self.assertEqual(self.tagger.ApplyCustomName(extrusion, ""), "Objeto 1")

    def test_spoken_name_is_sanitised(self) -> None:
        from tagger import Tagger

        self.assertEqual(Tagger.SanitizeSpokenName("  mesa   chica "), "mesa chica")
        self.assertEqual(Tagger.SanitizeSpokenName("¡mesa!"), "mesa")
        self.assertEqual(Tagger.SanitizeSpokenName(""), "")


# ---------------------------------------------------------------------------
# ObjectSelection: encontrar por el nombre dictado
# ---------------------------------------------------------------------------


class SelectByLabelTests(unittest.TestCase):
    """Lenient label matching for voice selection (§13)."""

    def setUp(self) -> None:
        self.document = FakeDocument([
            FakeObject("Box", "mesa"),
            FakeObject("Box001", "Mesa Chica"),
            FakeObject("Cyl", "Columna"),
        ])
        _install_freecad_stub(self.document)

        # object_selection lee FreeCAD al importarse: recargar con el stub puesto
        if str(SELECTION_ROOT) not in sys.path:
            sys.path.insert(0, str(SELECTION_ROOT))
        sys.modules.pop("object_selection", None)
        import importlib

        ObjectSelection = importlib.import_module("object_selection").ObjectSelection

        self.selector = ObjectSelection()

    def test_exact_match(self) -> None:
        self.assertEqual(self.selector.SelectByLabel("mesa"), "Box")

    def test_ignores_case(self) -> None:
        self.assertEqual(self.selector.SelectByLabel("MESA"), "Box")

    def test_ignores_accents(self) -> None:
        self.assertEqual(self.selector.SelectByLabel("cólumna"), "Cyl")

    def test_ignores_spaces(self) -> None:
        self.assertEqual(self.selector.SelectByLabel("mesachica"), "Box001")

    def test_exact_match_wins_over_prefix(self) -> None:
        """"mesa" must not be captured by "Mesa Chica"."""
        self.assertEqual(self.selector.SelectByLabel("mesa"), "Box")

    def test_unknown_name_returns_none(self) -> None:
        self.assertIsNone(self.selector.SelectByLabel("inexistente"))

    def test_empty_text_returns_none(self) -> None:
        self.assertIsNone(self.selector.SelectByLabel(""))


# ---------------------------------------------------------------------------
# StringInputPrompt: acumular entre frases
# ---------------------------------------------------------------------------


class _HeadlessPrompt:
    """StringInputPrompt's text logic without Qt.

    Building the real dialog needs a QApplication, and doing so without one
    aborts the interpreter (§13.d), so the methods the logic touches are
    replaced and only ProcessFinalText is exercised.
    """

    def __init__(self) -> None:
        from InputPrompts.PromptResult import PromptResult
        from InputPrompts.StringInputPrompt import StringInputPrompt

        self._AccumulatedText = ""
        self._Result = PromptResult.Pending()
        self.Status = ""
        self.Heard = ""
        self.ProcessFinalText = types.MethodType(
            StringInputPrompt.ProcessFinalText, self
        )
        self._StripConfirmation = StringInputPrompt._StripConfirmation
        self._HasConfirmation = StringInputPrompt._HasConfirmation
        self._HasCancellation = StringInputPrompt._HasCancellation

    def SetHeardText(self, text: str) -> None:
        self.Heard = text

    def SetStatus(self, status: str) -> None:
        self.Status = status

    def GetResult(self):
        return self._Result

    def AcceptValue(self, value=None):
        from InputPrompts.PromptResult import PromptResult

        self._Result = PromptResult.Ok(value)
        return self._Result

    def Cancel(self):
        from InputPrompts.PromptResult import PromptResult

        self._Result = PromptResult.Cancel()
        return self._Result

    def Fail(self, error: str):
        from InputPrompts.PromptResult import PromptResult

        self._Result = PromptResult.Fail(error)
        return self._Result


class StringPromptAccumulationTests(unittest.TestCase):
    """The prompt must accumulate across utterances (§17)."""

    @staticmethod
    def _say(*phrases: str):
        prompt = _HeadlessPrompt()
        result = prompt.GetResult()
        for phrase in phrases:
            result = prompt.ProcessFinalText(phrase)
        return result

    def test_name_and_confirmation_in_separate_phrases(self) -> None:
        """The bug: saying the name, pausing, then confirming used to fail."""
        result = self._say("rectangulo", "aceptar")
        self.assertTrue(result.Success)
        self.assertEqual(result.Value, "rectangulo")

    def test_name_and_confirmation_in_one_phrase(self) -> None:
        result = self._say("rectangulo aceptar")
        self.assertTrue(result.Success)
        self.assertEqual(result.Value, "rectangulo")

    def test_multi_word_name_dictated_in_parts(self) -> None:
        result = self._say("tapa", "superior", "aceptar")
        self.assertTrue(result.Success)
        self.assertEqual(result.Value, "tapa superior")

    def test_every_confirmation_synonym_works(self) -> None:
        """"confirmar" and "entrar" were dropped by the grammar bug (§16.a)."""
        for word in ("aceptar", "enviar", "confirmar", "entrar", "ok"):
            with self.subTest(word=word):
                result = self._say("rectangulo", word)
                self.assertTrue(result.Success, f"'{word}' no confirmó")
                self.assertEqual(result.Value, "rectangulo")

    def test_cancellation(self) -> None:
        result = self._say("rectangulo", "cancelar")
        self.assertTrue(result.Cancelled)

    def test_confirming_with_nothing_said_does_not_accept(self) -> None:
        result = self._say("aceptar")
        self.assertFalse(result.Success)


# ---------------------------------------------------------------------------
# Vocabulario de nombres
# ---------------------------------------------------------------------------


class ObjectNameVocabularyTests(unittest.TestCase):
    """Dav/dic/ObjectNames must offer the names the guide promises (§15)."""

    def test_spanish_vocabulary_has_the_expected_names(self) -> None:
        from ObjectNames.ObjectNames import GetObjectNamePhrases

        phrases = GetObjectNamePhrases("es")
        for word in ("cubo", "cuadrado", "mesa", "columna", "tapa", "eje"):
            with self.subTest(word=word):
                self.assertIn(word, phrases)

    def test_spoken_name_maps_to_written_label(self) -> None:
        from ObjectNames.ObjectNames import ResolveObjectName

        self.assertEqual(ResolveObjectName("cubo", "es"), "Cubo")

    def test_accented_and_plain_spellings_agree(self) -> None:
        """Vosk may return "rectángulo"; both must give the same label (§17.c)."""
        from ObjectNames.ObjectNames import ResolveObjectName

        self.assertEqual(
            ResolveObjectName("rectangulo", "es"),
            ResolveObjectName("rectángulo", "es"),
        )

    def test_unknown_word_resolves_to_empty(self) -> None:
        from ObjectNames.ObjectNames import ResolveObjectName

        self.assertEqual(ResolveObjectName("banana", "es"), "")

    def test_the_three_languages_are_populated(self) -> None:
        from ObjectNames.ObjectNames import GetObjectNamePhrases

        for lang in ("es", "en", "pt"):
            with self.subTest(lang=lang):
                self.assertTrue(GetObjectNamePhrases(lang))


# ---------------------------------------------------------------------------
# Gramáticas: lo que Vosk puede oír en cada pop-up
# ---------------------------------------------------------------------------


class GrammarContentTests(unittest.TestCase):
    """What reaches the recognizer, and what must stay out of it (§16)."""

    ENGLISH_WORDS = ("accept", "send", "enter", "confirm", "discard", "never mind")

    def test_new_name_grammar_excludes_other_languages(self) -> None:
        """English words crowded out "confirmar" and "entrar" (§16.a)."""
        from InputPrompts.NewObjectNameGrammarSwitcher import (
            NewObjectNameGrammarSwitcher,
        )

        phrases = NewObjectNameGrammarSwitcher.CollectNamePhrases("es")
        for word in self.ENGLISH_WORDS:
            with self.subTest(word=word):
                self.assertNotIn(word, phrases)

    def test_new_name_grammar_keeps_spanish_confirmations(self) -> None:
        from InputPrompts.NewObjectNameGrammarSwitcher import (
            NewObjectNameGrammarSwitcher,
        )

        phrases = NewObjectNameGrammarSwitcher.CollectNamePhrases("es")
        for word in ("aceptar", "enviar", "confirmar", "entrar", "ok"):
            with self.subTest(word=word):
                self.assertIn(word, phrases)

    def test_search_grammar_contains_user_labels(self) -> None:
        document = FakeDocument([FakeObject("Box", "Rectangulo")])
        _install_freecad_stub(document)

        from InputPrompts.ObjectNameGrammarSwitcher import ObjectNameGrammarSwitcher

        phrases = ObjectNameGrammarSwitcher.CollectLabelPhrases("es")
        self.assertIn("rectangulo", phrases)

    def test_search_grammar_drops_generated_sub_element_words(self) -> None:
        """Sub-elements drowned out the user's name (§16.b).

        A decomposed rectangle leaves "Linea 1".."Punto 4"; their individual
        words must not compete with the one name the user chose.
        """
        objects = [FakeObject("Box", "Rectangulo")]
        objects += [FakeObject(f"L{i}", f"Linea {i}") for i in range(1, 5)]
        objects += [FakeObject(f"P{i}", f"Punto {i}") for i in range(1, 5)]
        document = FakeDocument(objects)
        _install_freecad_stub(document)

        from InputPrompts.ObjectNameGrammarSwitcher import ObjectNameGrammarSwitcher

        phrases = ObjectNameGrammarSwitcher.CollectLabelPhrases("es")

        self.assertIn("rectangulo", phrases)
        for noise in ("linea", "punto", "1", "2", "3", "4"):
            with self.subTest(noise=noise):
                self.assertNotIn(noise, phrases)

        # pero siguen alcanzables por su etiqueta completa
        self.assertIn("linea 1", phrases)


class GrammarRoutingTests(unittest.TestCase):
    """Each prompt must request exactly one grammar (§15.c)."""

    def _prompts(self):
        from InputPrompts.IntegerInputPrompt import IntegerInputPrompt
        from InputPrompts.NewObjectNameInputPrompt import NewObjectNameInputPrompt
        from InputPrompts.ObjectNameInputPrompt import ObjectNameInputPrompt
        from InputPrompts.StringInputPrompt import StringInputPrompt

        def bare(cls, **attrs):
            obj = cls.__new__(cls)
            for key, value in attrs.items():
                setattr(obj, key, value)
            return obj

        return {
            "new_name": bare(NewObjectNameInputPrompt, _Language="es"),
            "search": bare(ObjectNameInputPrompt),
            "numeric": bare(IntegerInputPrompt),
            "plain": bare(StringInputPrompt),
        }

    def test_each_prompt_requests_exactly_one_grammar(self) -> None:
        from InputPrompts.PromptVoiceRouter import (
            _RequiresNewObjectNameGrammar,
            _RequiresNumericGrammar,
            _RequiresObjectNameGrammar,
        )

        checks = (
            _RequiresNumericGrammar,
            _RequiresObjectNameGrammar,
            _RequiresNewObjectNameGrammar,
        )
        expected = {
            "new_name": (False, False, True),
            "search": (False, True, False),
            "numeric": (True, False, False),
            "plain": (False, False, False),
        }

        for key, prompt in self._prompts().items():
            with self.subTest(prompt=key):
                self.assertEqual(
                    tuple(check(prompt) for check in checks), expected[key]
                )

    def test_no_prompt_means_no_grammar(self) -> None:
        from InputPrompts.PromptVoiceRouter import (
            _RequiresNewObjectNameGrammar,
            _RequiresNumericGrammar,
            _RequiresObjectNameGrammar,
        )

        for check in (
            _RequiresNumericGrammar,
            _RequiresObjectNameGrammar,
            _RequiresNewObjectNameGrammar,
        ):
            self.assertFalse(check(None))


# ---------------------------------------------------------------------------
# Diccionario de voz
# ---------------------------------------------------------------------------


class SelectionDictionaryTests(unittest.TestCase):
    """The spoken phrases that reach the new commands."""

    def test_byname_leaf_is_registered(self) -> None:
        from Selection.selection import selection

        self.assertIn("byname", selection)

    def test_byname_has_spoken_phrases(self) -> None:
        from Selection.selection import selection
        from Selection.TraduceToES import TraduceToEs

        target = selection["byname"]
        spoken = [k for k, v in TraduceToEs.items() if v is target]
        for phrase in ("buscar", "por nombre"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, spoken)

    def test_rectangle_has_synonyms_without_the_hard_word(self) -> None:
        """"rectangulo" was misheard as "ventana"/"banco"/"atras" (§14)."""
        from Workbench.Sketcher.Geometry.rectangle.rectangle import rectangle
        from Workbench.Sketcher.Geometry.rectangle.TraduceToEs import TraduceToEs

        target = rectangle["create_by_corners"]
        spoken = [k for k, v in TraduceToEs.items() if v is target]
        for phrase in ("por esquinas", "medidas", "coordenadas"):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, spoken)


if __name__ == "__main__":
    unittest.main(verbosity=2)

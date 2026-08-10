#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""
Unit tests for Browser — Developer 1 and Developer 2 coverage.

These tests use an in-memory MockDictionaryLoader so they do NOT depend on
any dictionary folder on disk (ejemplo de diccionario terminado is in .gitignore).

TODO Developer 3: add tests for descend and upward search once implemented.
TODO Developer 4: add integration tests with voice recognizer once implemented.
"""

from __future__ import annotations

import sys
import types
import unittest
from pathlib import Path
from typing import Any

GUI_ROOT = Path(__file__).resolve().parents[1]
def _find_repo_root(gui_root: Path) -> Path:
    # Mismo criterio que integration/dav_paths.py: Dav/scr/ se identifica por
    # validation/ y selection/, no por PruebaIntegracion/ (retirado a
    # Dav/docs/prototipos/).
    for parent in (gui_root.parents[1], gui_root.parents[2], gui_root.parents[0]):
        if (parent / "validation").is_dir() or (parent / "selection").is_dir():
            return parent
    return gui_root.parents[1]

REPO_ROOT = _find_repo_root(GUI_ROOT)

if str(GUI_ROOT) not in sys.path:
    sys.path.insert(0, str(GUI_ROOT))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _install_freecad_stub() -> None:
    if "FreeCADGui" not in sys.modules:
        gui = types.ModuleType("FreeCADGui")
        gui.runCommand = lambda name, idx=0: None  # type: ignore[attr-defined]
        sys.modules["FreeCADGui"] = gui
    if "FreeCAD" not in sys.modules:
        sys.modules["FreeCAD"] = types.ModuleType("FreeCAD")


# ---------------------------------------------------------------------------
# In-memory mock loader — no filesystem required
# ---------------------------------------------------------------------------

class _MockDictionaryLoader:
    """
    Simulates DictionaryLoader with in-memory dicts.
    Lets tests run without any dictionary folder on disk.
    """

    IsReady = True

    def __init__(self) -> None:
        self.DictionaryRoot = Path("/mock/dict")

        # Minimal command tree
        self._print_cmds: dict[str, Any] = {
            "print": lambda: None,
            "pdf":   lambda: None,
        }
        self._explorer: dict[str, Any] = {
            "print":   self._print_cmds,
            "refresh": lambda: None,
        }
        self._base_module: dict[str, Any] = {
            "explorer": self._explorer,
        }
        self._base_translate_es = {
            "explorador": self._explorer,
            "dibujar":    self._explorer,
            "dibujo":     self._explorer,
        }
        self._base_translate_en = {
            "explorer": self._explorer,
            "Draft":    self._explorer,
        }
        self._explorer_translate_es = {
            "imprimir":  self._print_cmds,
            "refrescar": lambda: None,
        }
        self._print_translate_es = {
            "pdf":      lambda: None,
            "imprimir": lambda: None,
        }

        # NavCommands: mismos sentinels que Dav/dic/NavCommands/NavActions.py,
        # replicados en memoria para no depender del disco en los tests.
        def _go_up() -> None:
            return None

        def _show_context() -> None:
            return None

        def _send() -> None:
            return None

        def _cancel() -> None:
            return None

        self._nav_actions: dict[str, Any] = {
            "up": _go_up,
            "show_context": _show_context,
            "send": _send,
            "cancel": _cancel,
        }
        self._nav_translate_es = {
            "subir":    self._nav_actions["up"],
            "volver":   self._nav_actions["up"],
            "contexto": self._nav_actions["show_context"],
            # enviar/cancelar salen de NavCommands como cualquier otro comando,
            # ya no estan hardcodeados en GetSpokenPhrases.
            "enviar":   self._nav_actions["send"],
            "aceptar":  self._nav_actions["send"],
            "cancelar": self._nav_actions["cancel"],
        }

    def LoadBaseModuleDict(self) -> dict[str, Any]:
        return dict(self._base_module)

    def LoadModuleDictByName(self, module_name: str, attr_name: str) -> dict[str, Any]:
        if module_name == "NavCommands.NavActions" and attr_name == "NavActions":
            return dict(self._nav_actions)
        return {}

    def LoadTranslateMap(self, folder: Path, language: Any) -> dict[str, Any]:
        from core.language_code import LanguageCode

        name = folder.name
        if name == "NavCommands":
            return dict(self._nav_translate_es)
        if name in ("dict", "root") or folder == self.DictionaryRoot:
            if language is LanguageCode.En:
                return dict(self._base_translate_en)
            return dict(self._base_translate_es)
        if name == "explorer":
            return dict(self._explorer_translate_es)
        if name == "print":
            return dict(self._print_translate_es)
        return {}

    def LoadTranslateSpokenKeys(self, folder: Path, language: Any) -> list[str]:
        return list(self.LoadTranslateMap(folder, language).keys())

    def ResolveSubFolder(self, parent_folder: Path, internal_key: str, target: Any = None) -> Path:
        return Path(f"/mock/{internal_key}")

    @staticmethod
    def NormalizeSpoken(text: str) -> str:
        import unicodedata
        decomposed = unicodedata.normalize("NFKD", text)
        stripped = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
        return " ".join(stripped.lower().split())


# ---------------------------------------------------------------------------
# Tests — Developer 1 (Preferences)
# ---------------------------------------------------------------------------

class TestPreferences(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        _install_freecad_stub()

    def test_default_language_is_valid(self) -> None:
        from core.language_code import LanguageCode
        from core.preferences import Preferences

        p = Preferences()
        self.assertIsInstance(p.SetLanguage, LanguageCode)

    def test_set_language_changes_value(self) -> None:
        from core.language_code import LanguageCode
        from core.preferences import Preferences

        p = Preferences()
        p.SetLanguage = LanguageCode.En
        self.assertEqual(p.SetLanguage, LanguageCode.En)
        p.SetLanguage = LanguageCode.Es
        self.assertEqual(p.SetLanguage, LanguageCode.Es)
        p.SetLanguage = LanguageCode.PT
        self.assertEqual(p.SetLanguage, LanguageCode.PT)

    def test_language_change_callback_fires(self) -> None:
        from core.language_code import LanguageCode
        from core.preferences import Preferences

        p = Preferences()
        p.SetLanguage = LanguageCode.Es
        fired: list[tuple] = []
        p.RegisterLanguageChange(lambda prev, new: fired.append((prev, new)))
        p.SetLanguage = LanguageCode.En
        self.assertEqual(len(fired), 1)
        self.assertEqual(fired[0][1], LanguageCode.En)


# ---------------------------------------------------------------------------
# Tests — Developer 2 (Browser base + BaseContext + Keychain)
# ---------------------------------------------------------------------------

class TestBrowserDeveloper2(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        _install_freecad_stub()

    def _make_browser(self, language=None):
        from core.language_code import LanguageCode
        from core.preferences import Preferences
        from navigation.browser import Browser

        p = Preferences()
        p.SetLanguage = language or LanguageCode.Es
        return Browser(prefs=p, _loader=_MockDictionaryLoader()), p

    def test_base_context_loaded(self) -> None:
        browser, _ = self._make_browser()
        keys = {e.InternalKey for e in browser.BaseContext}
        self.assertIn("explorer", keys)

    def test_context_loaded_from_translate(self) -> None:
        browser, _ = self._make_browser()
        spoken = {e.Spoken for e in browser.Context}
        self.assertIn("explorador", spoken)

    def test_base_jump_explorador(self) -> None:
        browser, _ = self._make_browser()
        result = browser.ProcessPhrase("explorador")
        self.assertTrue(result.Success)
        self.assertEqual(result.Action, "base_jump")

    def test_base_jump_dibujo(self) -> None:
        browser, _ = self._make_browser()
        result = browser.ProcessPhrase("dibujo")
        self.assertTrue(result.Success)
        self.assertEqual(result.Action, "base_jump")

    def test_unknown_command_returns_not_found(self) -> None:
        """Commands not found anywhere return not_found."""
        browser, _ = self._make_browser()
        result = browser.ProcessPhrase("imprimir")
        self.assertFalse(result.Success)
        self.assertEqual(result.Action, "not_found")

    def test_language_change_reloads_base(self) -> None:
        from core.language_code import LanguageCode

        browser, prefs = self._make_browser(LanguageCode.Es)
        spoken_es = {e.Spoken for e in browser.Context}
        self.assertIn("explorador", spoken_es)

        prefs.SetLanguage = LanguageCode.En
        spoken_en = {e.Spoken for e in browser.Context}
        self.assertIn("explorer", spoken_en)
        self.assertNotIn("explorador", spoken_en)

    def test_no_crash_without_dictionary(self) -> None:
        """Browser must start cleanly even when dictionary folder is missing."""
        from core.preferences import Preferences
        from navigation.browser import Browser

        p = Preferences()
        browser = Browser(dictionary_root="/nonexistent/path", prefs=p)
        self.assertEqual(browser.BaseContext, [])
        self.assertEqual(browser.Context, [])

    def test_get_spoken_phrases(self) -> None:
        """GetSpokenPhrases returns current context, base, nav commands, and [unk]."""
        browser, _ = self._make_browser()
        phrases = browser.GetSpokenPhrases()
        self.assertIn("explorador", phrases)
        self.assertIn("subir", phrases)
        self.assertIn("enviar", phrases)
        self.assertIn("cancelar", phrases)
        self.assertIn("[unk]", phrases)

    def test_nav_words_come_from_dictionary(self) -> None:
        """Confirm/cancel words are read from NavCommands, not hardcoded."""
        browser, _ = self._make_browser()
        self.assertEqual(browser.GetNavWords("send"), {"enviar", "aceptar"})
        self.assertEqual(browser.GetNavWords("cancel"), {"cancelar"})
        self.assertEqual(browser.GetNavWords("up"), {"subir", "volver"})
        # Un sentinel inexistente no rompe: devuelve vacio.
        self.assertEqual(browser.GetNavWords("nope"), set())

    def test_context_change_callback_fires(self) -> None:
        """on_context_change callback fires when descending or ascending context."""
        from core.language_code import LanguageCode
        from core.preferences import Preferences
        from navigation.browser import Browser

        changes: list[int] = []
        p = Preferences()
        p.SetLanguage = LanguageCode.Es
        b = Browser(prefs=p, _loader=_MockDictionaryLoader(), on_context_change=lambda: changes.append(1))
        # Initial ResetFromBase in __init__ fires callback
        self.assertGreaterEqual(len(changes), 1)

        count_before = len(changes)
        b.ProcessPhrase("explorador")
        b.ProcessPhrase("imprimir")
        self.assertGreater(len(changes), count_before)


# ---------------------------------------------------------------------------
# Tests — Developer 3 (Descend and Ascend)
# ---------------------------------------------------------------------------

class TestBrowserDeveloper3(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        _install_freecad_stub()

    def _make_browser(self):
        from core.language_code import LanguageCode
        from core.preferences import Preferences
        from navigation.browser import Browser

        p = Preferences()
        p.SetLanguage = LanguageCode.Es
        return Browser(prefs=p, _loader=_MockDictionaryLoader())

    def test_descend_to_subcontext(self) -> None:
        browser = self._make_browser()
        browser.ProcessPhrase("explorador")
        
        # say 'imprimir' -> descends to print (not a base command)
        res = browser.ProcessPhrase("imprimir")
        self.assertTrue(res.Success)
        self.assertEqual(res.Action, "descend")
        self.assertEqual(len(browser._stack), 3)
        self.assertEqual(browser._stack[-1].InternalName, "print")

    def test_execute_in_subcontext(self) -> None:
        browser = self._make_browser()
        browser.ProcessPhrase("explorador")
        
        # now inside explorer, say 'refrescar'
        res = browser.ProcessPhrase("refrescar")
        self.assertTrue(res.Success)
        self.assertEqual(res.Action, "execute")

    def test_search_upward_and_execute(self) -> None:
        browser = self._make_browser()
        browser.ProcessPhrase("explorador")
        browser.ProcessPhrase("imprimir")
        # now inside print (depth 3)
        self.assertEqual(len(browser._stack), 3)
        self.assertEqual(browser._stack[-1].InternalName, "print")
        
        # say 'refrescar' (exists in explorer, which is depth 2)
        res = browser.ProcessPhrase("refrescar")
        self.assertTrue(res.Success)
        self.assertEqual(res.Action, "execute")
        # stack should have been popped back to explorer
        self.assertEqual(len(browser._stack), 2)
        self.assertEqual(browser._stack[-1].InternalName, "explorer")

    def test_search_upward_not_found_reverts_context(self) -> None:
        browser = self._make_browser()
        browser.ProcessPhrase("explorador")
        browser.ProcessPhrase("imprimir")
        
        # save original context
        original_ctx = browser._SnapshotContext(browser.Context)
        
        # say completely unknown command
        res = browser.ProcessPhrase("unknown")
        self.assertFalse(res.Success)
        self.assertEqual(res.Action, "not_found")
        
        # should revert to what it was
        self.assertEqual(len(browser.Context), len(original_ctx))
        self.assertEqual(browser.Context[0].InternalKey, original_ctx[0].InternalKey)


# ---------------------------------------------------------------------------
# Tests — NavCommands (subir / mostrar contexto, no hardcodeados)
# ---------------------------------------------------------------------------

class TestBrowserNavCommands(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        _install_freecad_stub()

    def _make_browser(self):
        from core.language_code import LanguageCode
        from core.preferences import Preferences
        from navigation.browser import Browser

        p = Preferences()
        p.SetLanguage = LanguageCode.Es
        return Browser(prefs=p, _loader=_MockDictionaryLoader())

    def test_subir_ascends_like_old_volver(self) -> None:
        """'subir' viene de NavCommands/TraduceToEs.py, no de un set fijo."""
        browser = self._make_browser()
        browser.ProcessPhrase("explorador")
        self.assertEqual(len(browser._stack), 2)

        res = browser.ProcessPhrase("subir")
        self.assertTrue(res.Success)
        self.assertEqual(res.Action, "back")
        self.assertEqual(len(browser._stack), 1)

    def test_volver_still_ascends(self) -> None:
        """El viejo sinónimo 'volver' sigue andando vía NavCommands."""
        browser = self._make_browser()
        browser.ProcessPhrase("explorador")
        res = browser.ProcessPhrase("volver")
        self.assertTrue(res.Success)
        self.assertEqual(res.Action, "back")

    def test_up_at_root_fails(self) -> None:
        browser = self._make_browser()
        res = browser.ProcessPhrase("subir")
        self.assertFalse(res.Success)
        self.assertEqual(res.Action, "back")

    def test_contexto_describes_current_context(self) -> None:
        """'contexto' dispara ShowContext y no ejecuta ningún comando FreeCAD."""
        browser = self._make_browser()
        browser.ProcessPhrase("explorador")
        stack_before = len(browser._stack)

        res = browser.ProcessPhrase("contexto")
        self.assertTrue(res.Success)
        self.assertEqual(res.Action, "show_context")
        self.assertIn("Contexto", res.Message)
        # No debe haber navegado ni ejecutado nada
        self.assertEqual(len(browser._stack), stack_before)


if __name__ == "__main__":
    unittest.main()

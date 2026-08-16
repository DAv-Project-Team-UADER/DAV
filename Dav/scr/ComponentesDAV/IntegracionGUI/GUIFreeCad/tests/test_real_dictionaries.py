#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""
Integration tests for real dictionary hierarchy (Dav/dic).

Enforces Rule 4 (Nested subcontexts convention):
- Submenus MUST be nested under their own key (e.g. explorer.update({'file': file})).
- Submenus MUST NOT be flattened (e.g. explorer.update(file) is forbidden).
- Ensures no dead code overrides dictionary updates.
- Verifies base.py loads cleanly and subfolders remain navigable.
"""

from __future__ import annotations

import ast
import os
import sys
import types
import unittest
from pathlib import Path

GUI_ROOT = Path(__file__).resolve().parents[1]
if str(GUI_ROOT) not in sys.path:
    sys.path.insert(0, str(GUI_ROOT))

from integration.dav_paths import dav_repo_root, ensure_dav_repo_on_path  # noqa: E402

ensure_dav_repo_on_path()
DAV_DIR = dav_repo_root().parent
DIC_ROOT = DAV_DIR / "dic"

if str(DIC_ROOT) not in sys.path:
    sys.path.insert(0, str(DIC_ROOT))


def _install_freecad_stub() -> None:
    if "FreeCADGui" not in sys.modules:
        gui = types.ModuleType("FreeCADGui")
        gui.runCommand = lambda name, idx=0: None  # type: ignore[attr-defined]
        sys.modules["FreeCADGui"] = gui
    if "FreeCAD" not in sys.modules:
        sys.modules["FreeCAD"] = types.ModuleType("FreeCAD")
    app = sys.modules["FreeCAD"]
    if not hasattr(app, "ActiveDocument"):
        app.ActiveDocument = None
    class Vector:
        def __init__(self, *args, **kwargs): pass
    class Placement:
        def __init__(self, *args, **kwargs): pass
    class Rotation:
        def __init__(self, *args, **kwargs): pass
    class Matrix:
        def __init__(self, *args, **kwargs): pass
    for attr, cls in [("Vector", Vector), ("Placement", Placement), ("Rotation", Rotation), ("Matrix", Matrix)]:
        if not hasattr(app, attr):
            setattr(app, attr, cls)
    for mod in ("Part", "PartDesign", "Sketcher", "Draft", "TechDraw", "Assembly", "Mesh", "Fem"):
        if mod not in sys.modules:
            sys.modules[mod] = types.ModuleType(mod)


class TestRealDictionariesConvention(unittest.TestCase):
    """Audits Dav/dic for mandatory nesting convention and navigation integrity."""

    @classmethod
    def setUpClass(cls) -> None:
        _install_freecad_stub()

    def test_no_flattened_updates_in_dic(self) -> None:
        """
        Rule 4: Verify that no .update() call in Dav/dic flattens a sub-dictionary.
        All update calls must pass a dict literal mapping a key string to a sub-dict,
        e.g., dict.update({'key': sub_dict}).
        """
        violations: list[str] = []

        for root, _, files in os.walk(DIC_ROOT):
            for file in files:
                if not file.endswith(".py"):
                    continue
                filepath = Path(root) / file
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    source = f.read()

                try:
                    tree = ast.parse(source, filename=str(filepath))
                except SyntaxError as e:
                    violations.append(f"Syntax error in {filepath}: {e}")
                    continue

                for node in ast.walk(tree):
                    if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                        call = node.value
                        if isinstance(call.func, ast.Attribute) and call.func.attr == "update":
                            if len(call.args) == 1:
                                arg = call.args[0]
                                # If argument is a variable/name or call instead of a dict literal {}, record violation
                                if not isinstance(arg, ast.Dict):
                                    rel_path = filepath.relative_to(DIC_ROOT)
                                    violations.append(
                                        f"{rel_path}:{node.lineno} -> {ast.unparse(call)} "
                                        f"(Flattened update! Must wrap in dict literal like update({{'key': sub_dict}}))"
                                    )

        self.assertEqual(
            violations,
            [],
            "Found flattened .update(...) calls violating Rule 4:\n" + "\n".join(violations),
        )

    def test_base_py_imports_and_has_top_level_keys(self) -> None:
        """Verify that base.py loads clean top level dictionaries."""
        from navigation.dictionary_loader import DictionaryLoader

        loader = DictionaryLoader(DIC_ROOT)
        self.assertTrue(loader.IsReady, f"DictionaryLoader should find DIC_ROOT at {DIC_ROOT}")

        base_dict = loader.LoadBaseModuleDict()
        self.assertIn("explorer", base_dict)
        self.assertIn("stdview", base_dict)
        self.assertIn("workbench", base_dict)
        self.assertIn("lineattributes", base_dict)
        self.assertIn("preferences", base_dict)

    def test_top_level_workbenches_are_nested(self) -> None:
        """Verify that workbench.py contains nested workbenches as subcontext dicts."""
        from navigation.dictionary_loader import DictionaryLoader

        loader = DictionaryLoader(DIC_ROOT)
        base_dict = loader.LoadBaseModuleDict()
        workbench = base_dict.get("workbench", {})

        expected_submenus = ["assembly", "draft", "part", "partdesign", "sketcher", "techdraw"]
        for submenu in expected_submenus:
            self.assertIn(
                submenu,
                workbench,
                f"Workbench missing nested key '{submenu}'. Check workbench.py nesting!",
            )
    def test_techdraw_and_geometry_translations_populated(self) -> None:
        """Verify that TechDraw and Sketcher/Geometry translations are populated and not empty stubs."""
        from navigation.dictionary_loader import DictionaryLoader
        from core.language_code import LanguageCode

        loader = DictionaryLoader(DIC_ROOT)

        techdraw_dir = DIC_ROOT / "Workbench" / "TechDraw"
        es_map = loader.LoadTranslateMap(techdraw_dir, LanguageCode.Es)
        self.assertGreater(
            len(es_map),
            0,
            "TechDraw TraduceToEs.py is empty or invalid! Spoken commands in Spanish won't work.",
        )
        self.assertIn("vistas", es_map)
        self.assertIn("cotas", es_map)

        geometry_dir = DIC_ROOT / "Workbench" / "Sketcher" / "Geometry"
        en_geo_map = loader.LoadTranslateMap(geometry_dir, LanguageCode.En)
        pt_geo_map = loader.LoadTranslateMap(geometry_dir, LanguageCode.PT)
        self.assertGreater(len(en_geo_map), 0, "Sketcher/Geometry TraduceToEn.py is empty!")
        self.assertGreater(len(pt_geo_map), 0, "Sketcher/Geometry TraduceToPt.py is empty!")


if __name__ == "__main__":
    unittest.main()

#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""
Tests for Draft dictionaries (Dav/dic/Workbench/DraftWork).

Los comandos ``Draft_*`` solo existen una vez que el workbench Draft fue
inicializado. Estos tests aseguran que cada callable del árbol Draft activa el
workbench antes de ejecutar su comando (bug: "No such command 'Draft_Circle'").
"""

from __future__ import annotations

import importlib
import sys
import types
import unittest
from pathlib import Path

GUI_ROOT = Path(__file__).resolve().parents[1]
if str(GUI_ROOT) not in sys.path:
    sys.path.insert(0, str(GUI_ROOT))

from integration.dav_paths import dav_repo_root, ensure_dav_repo_on_path  # noqa: E402

ensure_dav_repo_on_path()
DIC_ROOT = dav_repo_root().parent / "dic"
if str(DIC_ROOT) not in sys.path:
    sys.path.insert(0, str(DIC_ROOT))

# Submenús de DraftWork que ejecutan comandos Draft_* vía runDraftCommand.
DRAFT_SUBMENUS = {
    "annotation_style_editor": "annotation",
    "annotation": "annotation",
    "arc": "arc",
    "circle": "circle",
    "circular_array": "array",
    "creation": "creation",
    "curve": "curve",
    "dimension": "dimension",
    "drafting": "drafting",
    "ellipse": "ellipse",
    "facebinder": "facebinder",
    "modification": "modification",
    "modify": "modify",
}


class _FakeGui:
    """FreeCADGui falso: registra llamadas y simula comandos aún no registrados."""

    def __init__(self) -> None:
        self.active = "StartWorkbench"
        self.calls: list[tuple] = []

    def reset(self, active: str = "StartWorkbench") -> None:
        self.active = active
        self.calls = []

    def activeWorkbench(self):
        gui = self

        class _Workbench:
            def name(self_inner) -> str:
                return gui.active

        return _Workbench()

    def activateWorkbench(self, name: str) -> None:
        self.calls.append(("activate", name))
        self.active = name

    def runCommand(self, name: str, idx: int = 0) -> None:
        # Igual que FreeCAD: Draft_* no existe hasta activar Draft.
        if name.startswith("Draft_") and self.active != "DraftWorkbench":
            raise Exception(f"No such command '{name}'")
        self.calls.append(("run", name))


class _FakeCreateObjects:
    def __init__(self, *args, **kwargs) -> None:
        pass

    def Execute(self) -> None:
        pass


def _install_stubs(fake_gui: _FakeGui) -> None:
    sys.modules["FreeCADGui"] = fake_gui  # type: ignore[assignment]
    app = sys.modules.get("FreeCAD") or types.ModuleType("FreeCAD")
    app.ActiveDocument = None
    sys.modules["FreeCAD"] = app
    for mod in ("Part", "Draft"):
        sys.modules.setdefault(mod, types.ModuleType(mod))
    createobjects = types.ModuleType("selection.createobjects")
    createobjects.CreateObjects = _FakeCreateObjects  # type: ignore[attr-defined]
    sys.modules.setdefault("selection.createobjects", createobjects)
    sys.modules.setdefault("createobjects", createobjects)


class TestDraftWorkbenchActivation(unittest.TestCase):
    """Cada comando Draft debe activar DraftWorkbench antes de ejecutarse."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.gui = _FakeGui()
        _install_stubs(cls.gui)
        for name in [m for m in sys.modules if m.startswith("Workbench.DraftWork")]:
            del sys.modules[name]
        cls.helper = importlib.import_module("Workbench.DraftWork.draftcommand")
        cls.helper.Gui = cls.gui

    def setUp(self) -> None:
        self.gui.reset()

    def test_helper_activates_draft_when_inactive(self) -> None:
        self.helper.runDraftCommand("Draft_Circle")
        self.assertEqual(
            self.gui.calls,
            [("activate", "DraftWorkbench"), ("run", "Draft_Circle")],
        )

    def test_helper_skips_activation_when_draft_already_active(self) -> None:
        self.gui.reset(active="DraftWorkbench")
        self.helper.runDraftCommand("Draft_Circle")
        self.assertEqual(self.gui.calls, [("run", "Draft_Circle")])

    def test_helper_activates_when_active_workbench_unavailable(self) -> None:
        def _boom():
            raise RuntimeError("sin workbench activo")

        self.gui.activeWorkbench = _boom  # type: ignore[method-assign]
        try:
            self.helper.runDraftCommand("Draft_Circle")
        finally:
            del self.gui.activeWorkbench
        self.assertEqual(self.gui.calls[0], ("activate", "DraftWorkbench"))

    def test_every_draft_callable_activates_workbench_first(self) -> None:
        checked = 0
        for folder, key in DRAFT_SUBMENUS.items():
            module = importlib.import_module(f"Workbench.DraftWork.{folder}.{folder}")
            module.runDraftCommand.__globals__["Gui"] = self.gui
            menu = getattr(module, key)
            for command, func in menu.items():
                if command == "help" or not callable(func):
                    continue
                if command.startswith("createobjects"):
                    continue  # no ejecuta comandos Draft, solo mapea el objeto activo
                with self.subTest(menu=folder, command=command):
                    self.gui.reset(active="StartWorkbench")
                    func()  # con la regresión levantaría "No such command"
                    runs = [c for c in self.gui.calls if c[0] == "run"]
                    self.assertTrue(runs, "no ejecutó ningún comando")
                    self.assertEqual(self.gui.calls[0], ("activate", "DraftWorkbench"))
                    checked += 1
        self.assertGreater(checked, 40)


if __name__ == "__main__":
    unittest.main()

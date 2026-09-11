#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Tests for idempotent visibility controls of the DAV dock."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


GUI_ROOT = Path(__file__).resolve().parents[1]
if str(GUI_ROOT) not in sys.path:
    sys.path.insert(0, str(GUI_ROOT))


class _FakeDock:
    def __init__(self, visible: bool) -> None:
        self.visible = visible
        self.show_calls = 0
        self.hide_calls = 0
        self.raise_calls = 0

    def isVisible(self) -> bool:
        return self.visible

    def show(self) -> None:
        self.show_calls += 1
        self.visible = True

    def hide(self) -> None:
        self.hide_calls += 1
        self.visible = False

    def raise_(self) -> None:
        self.raise_calls += 1


class TestDavDockPanelVisibility(unittest.TestCase):
    """Verify explicit DAV panel visibility actions."""

    def setUp(self) -> None:
        from integration import dav_dock_panel

        self.module = dav_dock_panel
        self.previous_dock = self.module._dock

    def tearDown(self) -> None:
        self.module._dock = self.previous_dock

    def test_hide_dav_panel_hides_visible_dock(self) -> None:
        self.assertTrue(hasattr(self.module, "hide_dav_panel"))
        dock = _FakeDock(visible=True)
        self.module._dock = dock

        self.module.hide_dav_panel()

        self.assertFalse(dock.visible)
        self.assertEqual(dock.hide_calls, 1)

    def test_show_dav_panel_shows_and_foregrounds_hidden_dock(self) -> None:
        self.assertTrue(hasattr(self.module, "show_dav_panel"))
        dock = _FakeDock(visible=False)
        self.module._dock = dock

        self.module.show_dav_panel()

        self.assertTrue(dock.visible)
        self.assertEqual(dock.show_calls, 1)
        self.assertEqual(dock.raise_calls, 1)


if __name__ == "__main__":
    unittest.main()

#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Tests for idempotent visibility controls of the DAV dock."""

from __future__ import annotations

import sys
import types
import unittest
from pathlib import Path
from unittest import mock


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


class _FakeDockWithActivate(_FakeDock):
    def __init__(self, visible: bool) -> None:
        super().__init__(visible)
        self.activate_calls = 0

    def activateWindow(self) -> None:
        self.activate_calls += 1


class TestDavDockPanelVisibility(unittest.TestCase):
    """Verify explicit DAV panel visibility actions."""

    def setUp(self) -> None:
        from integration import dav_dock_panel

        self.module = dav_dock_panel
        self.previous_dock = self.module._dock
        # Preserve any existing voice_bootstrap mock in sys.modules.
        self._voice_bootstrap_key = "integration.voice_bootstrap"
        self._prev_voice_bootstrap = sys.modules.get(self._voice_bootstrap_key)

    def tearDown(self) -> None:
        self.module._dock = self.previous_dock
        if self._prev_voice_bootstrap is not None:
            sys.modules[self._voice_bootstrap_key] = self._prev_voice_bootstrap
        elif self._voice_bootstrap_key in sys.modules:
            # If tests inserted a fake module, remove it to restore global state.
            # Keep real module if it was there before; our setUp saved None only
            # when there was no entry, so removal is correct.
            # When the real voice_bootstrap was loaded, it is kept in _prev.
            del sys.modules[self._voice_bootstrap_key]

    def test_hide_dav_panel_hides_visible_dock(self) -> None:
        self.assertTrue(hasattr(self.module, "hide_dav_panel"))
        dock = _FakeDock(visible=True)
        self.module._dock = dock

        result = self.module.hide_dav_panel()

        self.assertFalse(dock.visible)
        self.assertEqual(dock.hide_calls, 1)
        self.assertTrue(result)

    def test_hide_dav_panel_idempotent(self) -> None:
        dock = _FakeDock(visible=True)
        self.module._dock = dock

        self.module.hide_dav_panel()
        # Second hide must not break state or raise.
        result = self.module.hide_dav_panel()

        self.assertFalse(dock.visible)
        self.assertEqual(dock.hide_calls, 2)
        self.assertTrue(result)

    def test_hide_dav_panel_when_none_is_noop(self) -> None:
        self.module._dock = None
        # Must not raise; return False indicates nothing to hide.
        result = self.module.hide_dav_panel()
        self.assertFalse(result)
        self.assertIsNone(self.module._dock)

    def test_show_dav_panel_shows_and_foregrounds_hidden_dock(self) -> None:
        self.assertTrue(hasattr(self.module, "show_dav_panel"))
        dock = _FakeDock(visible=False)
        self.module._dock = dock

        result = self.module.show_dav_panel()

        self.assertTrue(dock.visible)
        self.assertEqual(dock.show_calls, 1)
        self.assertEqual(dock.raise_calls, 1)
        self.assertTrue(result)

    def test_show_dav_panel_idempotent(self) -> None:
        dock = _FakeDock(visible=False)
        self.module._dock = dock

        self.module.show_dav_panel()
        result = self.module.show_dav_panel()

        self.assertTrue(dock.visible)
        self.assertEqual(dock.show_calls, 2)
        self.assertEqual(dock.raise_calls, 2)
        self.assertTrue(result)

    def test_show_dav_panel_calls_activate_window_when_available(self) -> None:
        dock = _FakeDockWithActivate(visible=False)
        self.module._dock = dock

        result = self.module.show_dav_panel()

        self.assertTrue(dock.visible)
        self.assertEqual(dock.show_calls, 1)
        self.assertEqual(dock.raise_calls, 1)
        self.assertEqual(dock.activate_calls, 1)
        self.assertTrue(result)

    def test_show_dav_panel_without_activate_window_is_compatible(self) -> None:
        dock = _FakeDock(visible=False)
        # Ensure no activateWindow attribute
        self.assertFalse(hasattr(dock, "activateWindow"))
        self.module._dock = dock

        result = self.module.show_dav_panel()

        self.assertTrue(dock.visible)
        self.assertEqual(dock.show_calls, 1)
        self.assertEqual(dock.raise_calls, 1)
        self.assertTrue(result)

    def test_show_dav_panel_when_dock_is_none_tries_bootstrap(self) -> None:
        self.module._dock = None
        created = _FakeDockWithActivate(visible=False)

        def fake_show_dock_panel() -> bool:
            self.module._dock = created
            created.show()
            created.raise_()
            return True

        fake_module = types.ModuleType("integration.voice_bootstrap")
        fake_module.show_dock_panel = fake_show_dock_panel  # type: ignore[attr-defined]
        sys.modules[self._voice_bootstrap_key] = fake_module

        result = self.module.show_dav_panel()

        self.assertTrue(result)
        self.assertIs(self.module._dock, created)
        self.assertTrue(created.visible)
        # show_dock_panel already did show+raise; show_dav_panel adds activateWindow
        self.assertEqual(created.activate_calls, 1)

    def test_show_dav_panel_when_bootstrap_fails_returns_false(self) -> None:
        self.module._dock = None

        fake_module = types.ModuleType("integration.voice_bootstrap")
        fake_module.show_dock_panel = lambda: False  # type: ignore[attr-defined]
        sys.modules[self._voice_bootstrap_key] = fake_module

        with mock.patch.object(self.module, "_notify_panel_failure") as mock_notify:
            result = self.module.show_dav_panel()

        self.assertFalse(result)
        self.assertIsNone(self.module._dock)
        mock_notify.assert_called()

    def test_show_dav_panel_when_no_voice_engine_returns_false(self) -> None:
        self.module._dock = None

        # Simulate show_dock_panel that reports voice inactive (returns False)
        # and leaves _dock as None, as voice_bootstrap does when adapter is None.
        fake_module = types.ModuleType("integration.voice_bootstrap")
        fake_module.show_dock_panel = lambda: False  # type: ignore[attr-defined]
        sys.modules[self._voice_bootstrap_key] = fake_module

        with mock.patch.object(self.module, "_notify_panel_failure") as mock_notify:
            result = self.module.show_dav_panel()

        self.assertFalse(result)
        self.assertIsNone(self.module._dock)
        mock_notify.assert_called()

    def test_show_dav_panel_when_bootstrap_succeeds_but_dock_still_none(self) -> None:
        self.module._dock = None
        fake_module = types.ModuleType("integration.voice_bootstrap")
        # Returns True but forgets to set _dock (broken install)
        fake_module.show_dock_panel = lambda: True  # type: ignore[attr-defined]
        sys.modules[self._voice_bootstrap_key] = fake_module

        with mock.patch.object(self.module, "_notify_panel_failure") as mock_notify:
            result = self.module.show_dav_panel()

        self.assertFalse(result)
        mock_notify.assert_called()


if __name__ == "__main__":
    unittest.main()

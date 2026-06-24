# Copyright (C) 2026 El Equipo del Proyecto DAV
# SPDX-License-Identifier: GPL-3.0-or-later

"""Run all Validator tests (unit + integration)."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))


def main() -> int:
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.discover(str(ROOT), pattern="test_*.py"))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())

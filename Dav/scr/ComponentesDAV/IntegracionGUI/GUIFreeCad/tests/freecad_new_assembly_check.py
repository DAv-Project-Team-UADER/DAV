#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Headless check of ``new_assembly``; run with ``freecadcmd.exe freecad_new_assembly_check.py``.

Prints ``CHECK OK`` when the assembly is created, found by the other assembly
commands, not duplicated, and ``new_part`` works right after it.
"""

import sys
import traceback
from pathlib import Path

import FreeCAD as App

DIC = Path(__file__).resolve().parents[5] / "dic"
sys.path.insert(0, str(DIC))
sys.path.insert(0, str(DIC.parent))
sys.path.insert(0, str(DIC.parent / "scr" / "ComponentesDAV" / "IntegracionGUI" / "GUIFreeCad"))


# FreeCAD ya cargó el DAV instalado (AppData\...\Mod\DAV): se prueba el código de este repo
for name in [n for n in sys.modules if n == "dic" or n.startswith("dic.") or n == "Workbench" or n.startswith("Workbench.")]:
    del sys.modules[name]


def check(condition, message):
    if not condition:
        raise AssertionError(message)
    print("  ok:", message)


try:
    from dic.Workbench.Assembly import _parametric as asm

    doc = App.newDocument("check")
    check(asm._ActiveAssembly(doc) is None, "no assembly before creating one")

    asm.new_assembly()
    found = asm._ActiveAssembly(doc)
    check(found is not None, "_ActiveAssembly finds the assembly right after new_assembly")
    check(found.isDerivedFrom("Assembly::AssemblyObject"), "it is an Assembly::AssemblyObject")
    check(any(o.isDerivedFrom("Assembly::JointGroup") for o in found.Group), "it has its Joints group")

    asm.new_assembly()
    count = len([o for o in doc.Objects if o.isDerivedFrom("Assembly::AssemblyObject")])
    check(count == 1, "saying it twice does not create a second assembly")

    asm.new_part()
    check(doc.getObject("Pieza") is not None, "new_part works right after new_assembly")
    print("CHECK OK")
except Exception:
    traceback.print_exc()
    print("CHECK FAILED")
    sys.exit(1)

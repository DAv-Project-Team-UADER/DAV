#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Headless check of which Body a new PartDesign figure goes into.

Run with ``freecadcmd.exe freecad_active_body_check.py``. Sin ventana no hay cuerpo
activo, así que se simula reemplazando ``activeBody``. Imprime ``CHECK OK`` al terminar.
"""

import sys
import traceback
from pathlib import Path

import FreeCAD as App

DIC = Path(__file__).resolve().parents[5] / "dic"
for path in (DIC / ".." / "scr" / "ComponentesDAV" / "IntegracionGUI" / "GUIFreeCad", DIC.parent / "scr", DIC, DIC.parent):
    sys.path.insert(0, str(path.resolve()))

# FreeCAD ya cargó el DAV instalado (AppData\...\Mod\DAV): se prueba el código de este repo
for name in [n for n in sys.modules if n in ("dic", "Workbench") or n.startswith(("dic.", "Workbench."))]:
    del sys.modules[name]


def check(condition, message):
    if not condition:
        raise AssertionError(message)
    print("  ok:", message)


try:
    from dic.Workbench.PartDesign import _placement as pl
    from dic.Workbench.PartDesign.additive import _parametric as ad
    from dic.Workbench.PartDesign.additive import additive as add

    asked = []
    pl.askYesNo = lambda title, msg: asked.append(msg) or True
    pl.askObject = lambda *a, **k: asked.append("LIST") or None
    state = {"active": None}
    pl.activeBody = lambda doc: state["active"]
    add.activeBody = pl.activeBody

    def bodies(doc):
        return [o for o in doc.Objects if o.TypeId == "PartDesign::Body"]

    # 1. sin cuerpos ni cuerpo activo: crea uno y la figura se ejecuta
    doc = App.newDocument("a")
    state["active"] = None
    ad.cylinder_by_size(5, 10, 0, 0, 5)
    check(len(bodies(doc)) == 1 and not asked, "no body at all: one is created without asking")
    check(any(o.TypeId == "PartDesign::AdditiveCylinder" and o.isValid() for o in doc.Objects), "the cylinder is created and valid")

    # 2. cuerpo activo vacío: la figura va a ese, no se crea otro ni se pregunta
    doc = App.newDocument("b")
    empty = doc.addObject("PartDesign::Body", "Body")
    state["active"] = empty
    asked.clear()
    ad.cylinder_by_size(5, 10, 0, 0, 5)
    check(len(bodies(doc)) == 1, "an active empty body is used (no second body)")
    check(not asked, "nothing is asked when a body is active")
    check(any(o.TypeId == "PartDesign::AdditiveCylinder" for o in empty.Group), "the cylinder lives in the active body")

    # 3. otras figuras por medidas siguen el mismo camino
    ad.box_by_size(10, 10, 10, 0, 0, 5)
    check(any(o.TypeId == "PartDesign::AdditiveBox" for o in empty.Group), "a box also goes to the active body")

    # 4. primitiva sin medidas (additive_cylinder): también el cuerpo activo
    doc = App.newDocument("c")
    empty = doc.addObject("PartDesign::Body", "Body")
    state["active"] = empty
    add.additive_cylinder()
    check(len(bodies(doc)) == 1, "additive_cylinder uses the active body too")

    # 5. sin cuerpo activo y sin cuerpo: additive_cylinder crea uno
    doc = App.newDocument("d")
    state["active"] = None
    add.additive_cylinder()
    check(len(bodies(doc)) == 1, "additive_cylinder with no body creates one")

    # 6. sin cuerpo activo pero con cuerpos válidos: se conserva la pregunta (ejemplos guiados)
    doc = App.newDocument("e")
    solid = doc.addObject("PartDesign::Body", "Body")
    cyl = solid.newObject("PartDesign::AdditiveCylinder", "Cylinder")
    cyl.Radius, cyl.Height = 5, 10
    doc.recompute()
    state["active"] = None
    asked.clear()
    ad.cylinder_by_size(5, 10, 0, 0, 5)
    check(len(asked) == 1 and "cuerpo nuevo" in asked[0], "without an active body the 'new body?' question is kept")
    print("CHECK OK")
except Exception:
    traceback.print_exc()
    print("CHECK FAILED")
    sys.exit(1)

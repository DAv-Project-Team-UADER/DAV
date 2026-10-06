#  Copyright (C) 2026 The DAV Project Team
#  Universidad Autónoma de Entre Ríos (UADER)
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Headless check of the voice transformations; run with ``freecadcmd.exe freecad_transforms_check.py``.

Las respuestas de voz se simulan reemplazando los cuadros (``askChoice``, ``askNumber``,
``askObject``): lo que se prueba es la geometría que se crea y que no quede inválida.
Imprime ``CHECK OK`` al terminar sin fallas.
"""

import sys
import traceback
from pathlib import Path

import FreeCAD as App

DIC = Path(__file__).resolve().parents[5] / "dic"
sys.path.insert(0, str(DIC))
sys.path.insert(0, str(DIC.parent))
sys.path.insert(0, str(DIC.parent / "scr"))
sys.path.insert(0, str(DIC.parent / "scr" / "ComponentesDAV" / "IntegracionGUI" / "GUIFreeCad"))

# FreeCAD ya cargó el DAV instalado (AppData\...\Mod\DAV): se prueba el código de este repo
for name in [n for n in sys.modules if n == "dic" or n.startswith("dic.") or n == "Workbench" or n.startswith("Workbench.")]:
    del sys.modules[name]


def check(condition, message):
    if not condition:
        raise AssertionError(message)
    print("  ok:", message)


try:
    from dic.Workbench.PartDesign.transform import _parametric as tr

    doc = App.newDocument("check")
    body = doc.addObject("PartDesign::Body", "Body")
    cylinder = body.newObject("PartDesign::AdditiveCylinder", "Cylinder")
    cylinder.Radius, cylinder.Height = 5, 10
    doc.recompute()

    answers = {"choice": [], "number": []}
    tr.askChoice = lambda title, message, options: answers["choice"].pop(0)
    tr.askNumber = lambda title, message: answers["number"].pop(0)
    asked = []
    tr.askObject = lambda doc, title, message, flt, empty: asked.append(message) or cylinder

    # sin selección la lista ofrece solo operaciones repetibles
    check(tr._isRepeatable(cylinder), "an additive cylinder can be repeated")
    check(not tr._isRepeatable(body), "a body cannot be repeated")

    def only_new(type_id):
        return [o for o in doc.Objects if o.TypeId == type_id]

    answers["choice"] = ["X_Axis"]
    answers["number"] = [4, 60]
    tr.linear_pattern_voice()
    lin = only_new("PartDesign::LinearPattern")
    check(len(lin) == 1 and lin[0].Occurrences == 4 and lin[0].Length == 60, "linear pattern: 4 copies over 60 mm")
    check(lin[0].isValid(), "linear pattern is valid")
    check(lin[0].Direction[0].Role == "X_Axis", "linear pattern uses the body's X axis")
    check(lin[0].getParentGeoFeatureGroup() == body, "linear pattern lives in the body")

    answers["choice"] = ["Z_Axis"]
    answers["number"] = [6, 360]
    tr.polar_pattern_voice()
    pol = only_new("PartDesign::PolarPattern")
    check(len(pol) == 1 and pol[0].Occurrences == 6 and pol[0].Angle == 360, "polar pattern: 6 copies over 360 degrees")
    check(pol[0].isValid(), "polar pattern is valid")

    answers["choice"] = ["YZ_Plane"]
    tr.mirrored_voice()
    mir = only_new("PartDesign::Mirrored")
    check(len(mir) == 1 and mir[0].isValid(), "mirror across YZ is valid")
    check(mir[0].MirrorPlane[0].Role == "YZ_Plane", "mirror uses the body's YZ plane")

    answers["number"] = [2, 2]
    tr.scaled_voice()
    sca = only_new("PartDesign::Scaled")
    check(len(sca) == 1 and sca[0].Factor == 2 and sca[0].isValid(), "scaled by 2 is valid")

    check(len(asked) == 4, "with no selection each flow asked for the operation by list")

    # cancelaciones: nada queda creado
    before = len(doc.Objects)
    answers["choice"] = [None]
    answers["number"] = []
    tr.linear_pattern_voice()
    answers["choice"] = [None]
    tr.mirrored_voice()
    answers["choice"] = ["X_Axis"]
    answers["number"] = [1]
    tr.polar_pattern_voice()  # 1 copia no vale
    check(len(doc.Objects) == before, "cancelling or an invalid copy count creates nothing")

    print("CHECK OK")
except Exception:
    traceback.print_exc()
    print("CHECK FAILED")
    sys.exit(1)

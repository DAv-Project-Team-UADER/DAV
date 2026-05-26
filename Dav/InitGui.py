# DAV (UADER) — InitGui minimo: FreeCAD ejecuta este archivo en un namespace especial.
# Toda la logica esta en scr.gui.freecad_wb (import normal).

import os
import sys

import FreeCAD as App
import FreeCADGui as Gui

# Solo asignaciones: poner el mod en sys.path
_d = ""
for _p in getattr(App, "__ModDirs__", ()) or ():
    _n = os.path.normpath(_p)
    if os.path.basename(_n).upper() == "DAV":
        _d = _n
        break
if not _d:
    _e = os.environ.get("DAV_MOD_ROOT", "").strip()
    if _e and os.path.isdir(_e):
        _d = os.path.normpath(_e)
if not _d:
    _u = os.path.join(App.getUserAppDataDir(), "Mod", "DAV")
    if os.path.isdir(_u):
        _d = _u
if _d and _d not in sys.path:
    sys.path.insert(0, _d)


class DAVWorkbench(Gui.Workbench):
    MenuText = "DAV"
    ToolTip = "DAV (UADER)"

    def Initialize(self):
        import scr.gui.freecad_wb

        scr.gui.freecad_wb.setup_workbench(self)

    def GetClassName(self):
        return "Gui::PythonWorkbench"


# InitGui se ejecuta con exec(): no usar funciones auxiliares aqui.
_wb_registered = False
try:
    _wb_registered = Gui.getWorkbench("DAVWorkbench") is not None
except Exception:
    _wb_registered = False
if not _wb_registered:
    Gui.addWorkbench(DAVWorkbench())

if os.environ.get("DAV_AUTOLOAD_WORKBENCH") == "1":
    try:
        from PySide6.QtCore import QTimer
    except ImportError:
        from PySide2.QtCore import QTimer  # type: ignore[no-redef]

    QTimer.singleShot(500, lambda: Gui.activateWorkbench("DAVWorkbench"))

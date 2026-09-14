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
if _d:
    _d_real = os.path.realpath(_d)
    if _d_real not in sys.path:
        sys.path.insert(0, _d_real)
    _curr = _d_real
    for _ in range(4):
        _parent = os.path.dirname(_curr)
        if _parent == _curr:
            break
        found = False
        for name in ("ComponentesDAV", "componentesDAV"):
            if os.path.isdir(os.path.join(_parent, name)):
                if _parent not in sys.path:
                    sys.path.insert(0, _parent)
                try:
                    if name not in sys.modules:
                        mod = __import__(name)
                        sys.modules[name] = mod
                    other_name = "componentesDAV" if name == "ComponentesDAV" else "ComponentesDAV"
                    if other_name not in sys.modules and name in sys.modules:
                        sys.modules[other_name] = sys.modules[name]
                except Exception:
                    pass
                found = True
                break
        if found:
            break
        _curr = _parent


try:
    import scr.gui.dav_commands as _dav_commands

    _dav_commands._ensure_selection_path()
    _dav_commands._ensure_validation_path()
except Exception:
    pass


class DAVWorkbench(Gui.Workbench):
    MenuText = "DAV"
    ToolTip = "DAV (UADER)"

    def Initialize(self):
        import componentesDAV.Dav.scr.gui.freecad_wb

        componentesDAV.Dav.scr.gui.freecad_wb.setup_workbench(self)

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

if os.environ.get("DAV_AUTOLOAD_WORKBENCH") != "0":
    try:
        from PySide6.QtCore import QTimer
    except ImportError:
        from PySide2.QtCore import QTimer  # type: ignore[no-redef]

    def _activate_dav_workbench() -> None:
        try:
            Gui.activateWorkbench("DAVWorkbench")
        except Exception:
            import traceback

            App.Console.PrintError("[DAV] No se pudo activar el workbench DAV:\n")
            App.Console.PrintError(traceback.format_exc())

    QTimer.singleShot(500, _activate_dav_workbench)

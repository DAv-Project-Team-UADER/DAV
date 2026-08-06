import FreeCAD as App
import FreeCADGui as Gui

try:
    from createobjects import CreateObjects
except ImportError:
    from selection.createobjects import CreateObjects
from .ayuda import ayuda


def bezier():
    Gui.runCommand("Draft_BezCurve", 0)
    CreateObjects(Is3D=False).Execute(App.ActiveDocument.ActiveObject)


def bspline():
    Gui.runCommand("Draft_BSpline", 0)
    CreateObjects(Is3D=False).Execute(App.ActiveDocument.ActiveObject)


def cubic():
    Gui.runCommand("Draft_CubicBezCurve", 0)
    CreateObjects(Is3D=False).Execute(App.ActiveDocument.ActiveObject)


curve = {
    "bezier": bezier,
    "bspline": bspline,
    "cubic": cubic,
    "help": ayuda,
}

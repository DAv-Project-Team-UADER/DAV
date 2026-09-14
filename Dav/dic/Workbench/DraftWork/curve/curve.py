import FreeCAD as App
import FreeCADGui as Gui

try:
    from createobjects import CreateObjects
except ImportError:
    from selection.createobjects import CreateObjects
from .ayuda import ayuda


def bezier():
    Gui.runCommand("Draft_BezCurve", 0)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def bspline():
    Gui.runCommand("Draft_BSpline", 0)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def cubic():
    Gui.runCommand("Draft_CubicBezCurve", 0)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


curve = {
    "bezier": bezier,
    "bspline": bspline,
    "cubic": cubic,
    "help": ayuda,
}

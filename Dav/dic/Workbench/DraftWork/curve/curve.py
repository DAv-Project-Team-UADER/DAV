import FreeCAD as App

try:
    from createobjects import CreateObjects
except ImportError:
    from selection.createobjects import CreateObjects
from ..draftcommand import runDraftCommand
from .ayuda import ayuda


def bezier():
    runDraftCommand("Draft_BezCurve")
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def bspline():
    runDraftCommand("Draft_BSpline")
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def cubic():
    runDraftCommand("Draft_CubicBezCurve")
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


curve = {
    "bezier": bezier,
    "bspline": bspline,
    "cubic": cubic,
    "help": ayuda,
}

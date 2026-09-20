import FreeCAD as App

try:
    from createobjects import CreateObjects
except ImportError:
    from selection.createobjects import CreateObjects
from ..draftcommand import runDraftCommand
from .._parametric import bezier_by_points, bspline_by_points, cubic_by_points
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
    "bezier": bezier_by_points,
    "bspline": bspline_by_points,
    "cubic": cubic_by_points,
    "interactive_bezier": bezier,
    "interactive_bspline": bspline,
    "interactive_cubic": cubic,
    "help": ayuda,
}

import FreeCAD as App

try:
    from createobjects import CreateObjects
except ImportError:
    from selection.createobjects import CreateObjects
from ..draftcommand import runDraftCommand
from .._parametric import arc_by_3_points, arc_by_center
from .ayuda import ayuda


def center():
    runDraftCommand("Draft_Arc")
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def points():
    runDraftCommand("Draft_Arc_3Points")
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


arc = {
    "center": arc_by_center,
    "points": arc_by_3_points,
    "interactive": center,
    "interactive_points": points,
    "help": ayuda,
}

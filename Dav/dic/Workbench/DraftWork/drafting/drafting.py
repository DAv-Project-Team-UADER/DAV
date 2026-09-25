import FreeCAD as App

try:
    from createobjects import CreateObjects
except ImportError:
    from selection.createobjects import CreateObjects
from ..draftcommand import runDraftCommand
from .._parametric import line_by_points, wire_by_points
from .ayuda import ayuda


def wire():
    runDraftCommand("Draft_Wire")


def create_wire_objects():
    doc = App.ActiveDocument
    if doc is None or doc.ActiveObject is None:
        print("Error: no hay objeto activo para mapear.")
        return

    obj = doc.ActiveObject
    CreateObjects(ObjectName=obj.Name, Is3D=False).Execute()


drafting = {
    "wire": wire_by_points,
    "line": line_by_points,
    "interactive": wire,
    "createobjects": create_wire_objects,
    "createobjects2d": create_wire_objects,
    "help": ayuda,
}

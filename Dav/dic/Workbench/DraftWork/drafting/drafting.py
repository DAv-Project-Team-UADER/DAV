import FreeCAD as App

try:
    from createobjects import CreateObjects
except ImportError:
    from selection.createobjects import CreateObjects
from ..draftcommand import runDraftCommand
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
    "wire": wire,
    "createobjects": create_wire_objects,
    "createobjects2d": create_wire_objects,
    "help": ayuda,
}

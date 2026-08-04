import FreeCAD as App
import FreeCADGui as Gui

from createobjects import CreateObjects
from .ayuda import ayuda


def wire():
    Gui.runCommand("Draft_Wire", 0)


def create_wire_objects():
    doc = App.ActiveDocument
    if doc is None or doc.ActiveObject is None:
        print("Error: no hay objeto activo para mapear.")
        return

    obj = doc.ActiveObject
    CreateObjects(obj.Name, Is3D=False).execute()


drafting = {
    "wire": wire,
    "createobjects": create_wire_objects,
    "createobjects2d": create_wire_objects,
    "help": ayuda,
}

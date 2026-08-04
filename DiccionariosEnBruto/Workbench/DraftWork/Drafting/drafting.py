import FreeCAD as App
import FreeCADGui as Gui

from createobjects import CreateObjects
from .ayuda import ayuda


def wire():
    Gui.runCommand("Draft_Wire", 0)

    obj = App.ActiveDocument.ActiveObject
    CreateObjects(Is3D=False).Execute(obj)


drafting = {
    "wire": wire,
    "help": ayuda,
}

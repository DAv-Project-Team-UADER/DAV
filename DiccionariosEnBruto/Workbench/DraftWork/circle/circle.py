import FreeCAD as App
import FreeCADGui as Gui

from createobjects import CreateObjects
from .ayuda import ayuda

def center():
    Gui.runCommand("Draft_Circle", 0)

    obj = App.ActiveDocument.ActiveObject
    CreateObjects(Is3D=False).Execute(obj)

circle = {
    "center": center,
    "help": ayuda,
}

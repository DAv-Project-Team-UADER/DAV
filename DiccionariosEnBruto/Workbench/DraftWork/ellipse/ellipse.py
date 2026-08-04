import FreeCAD as App
import FreeCADGui as Gui

from createobjects import CreateObjects
from .ayuda import ayuda


def center():
    Gui.runCommand("Draft_Ellipse", 0)
    CreateObjects(Is3D=False).Execute(App.ActiveDocument.ActiveObject)


ellipse = {
    "center": center,
    "help": ayuda,
}

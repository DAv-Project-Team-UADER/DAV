import FreeCAD as App
import FreeCADGui as Gui

try:
    from createobjects import CreateObjects
except ImportError:
    from selection.createobjects import CreateObjects
from .ayuda import ayuda


def center():
    Gui.runCommand("Draft_Arc", 0)
    CreateObjects(Is3D=False).Execute(App.ActiveDocument.ActiveObject)


def points():
    Gui.runCommand("Draft_Arc_3Points", 0)
    CreateObjects(Is3D=False).Execute(App.ActiveDocument.ActiveObject)


arc = {
    "center": center,
    "points": points,
    "help": ayuda,
}

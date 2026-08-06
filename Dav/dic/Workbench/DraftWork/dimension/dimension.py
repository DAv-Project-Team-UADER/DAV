import FreeCAD as App
import FreeCADGui as Gui

try:
    from createobjects import CreateObjects
except ImportError:
    from selection.createobjects import CreateObjects
from .ayuda import ayuda


def linear():
    Gui.runCommand("Draft_Dimension", 0)
    CreateObjects(Is3D=False).Execute(App.ActiveDocument.ActiveObject)


dimension = {
    "linear": linear,
    "flip": lambda: Gui.runCommand("Draft_FlipDimension", 0),
    "help": ayuda,
}

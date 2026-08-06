import FreeCAD as App
import FreeCADGui as Gui

try:
    from createobjects import CreateObjects
except ImportError:
    from selection.createobjects import CreateObjects
from .ayuda import ayuda


def create():
    Gui.runCommand("Draft_Facebinder", 0)
    CreateObjects(Is3D=False).Execute(App.ActiveDocument.ActiveObject)


facebinder = {
    "create": create,
    "help": ayuda,
}

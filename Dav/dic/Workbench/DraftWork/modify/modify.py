import FreeCAD as App
import FreeCADGui as Gui

try:
    from createobjects import CreateObjects
except ImportError:
    from selection.createobjects import CreateObjects
from .ayuda import ayuda


def clone():
    Gui.runCommand("Draft_Clone", 0)
    CreateObjects(Is3D=False).Execute(App.ActiveDocument.ActiveObject)


def sketch():
    Gui.runCommand("Draft_Draft2Sketch", 0)
    CreateObjects(Is3D=False).Execute(App.ActiveDocument.ActiveObject)


def offset():
    Gui.runCommand("Draft_Offset", 0)
    CreateObjects(Is3D=False).Execute(App.ActiveDocument.ActiveObject)


modify = {
    "clone": clone,
    "downgrade": lambda: Gui.runCommand("Draft_Downgrade", 0),
    "sketch": sketch,
    "edit": lambda: Gui.runCommand("Draft_Edit", 0),
    "fillet": lambda: Gui.runCommand("Draft_Fillet", 0),
    "join": lambda: Gui.runCommand("Draft_Join", 0),
    "move": lambda: Gui.runCommand("Draft_Move", 0),
    "offset": offset,
    "rotate": lambda: Gui.runCommand("Draft_Rotate", 0),
    "mirror": lambda: Gui.runCommand("Draft_Mirror", 0),
    "help": ayuda,
}

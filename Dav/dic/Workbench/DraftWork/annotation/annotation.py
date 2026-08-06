import FreeCAD as App
import FreeCADGui as Gui

try:
    from createobjects import CreateObjects
except ImportError:
    from selection.createobjects import CreateObjects
from .ayuda import ayuda


def text():
    Gui.runCommand("Draft_Text", 0)
    CreateObjects(Is3D=False).Execute(App.ActiveDocument.ActiveObject)


def shapestring():
    Gui.runCommand("Draft_ShapeString", 0)
    CreateObjects(Is3D=False).Execute(App.ActiveDocument.ActiveObject)


def label():
    Gui.runCommand("Draft_Label", 0)
    CreateObjects(Is3D=False).Execute(App.ActiveDocument.ActiveObject)


annotation = {
    "text": text,
    "shapestring": shapestring,
    "label": label,
    "help": ayuda,
}

import FreeCAD as App
import FreeCADGui as Gui

try:
    from createobjects import CreateObjects
except ImportError:
    from selection.createobjects import CreateObjects
from .ayuda import ayuda


def center():
    Gui.runCommand("Draft_Arc", 0)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def points():
    Gui.runCommand("Draft_Arc_3Points", 0)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


arc = {
    "center": center,
    "points": points,
    "help": ayuda,
}

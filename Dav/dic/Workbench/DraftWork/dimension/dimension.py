import FreeCAD as App

try:
    from createobjects import CreateObjects
except ImportError:
    from selection.createobjects import CreateObjects
from ..draftcommand import runDraftCommand
from .ayuda import ayuda


def linear():
    runDraftCommand("Draft_Dimension")
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


dimension = {
    "linear": linear,
    "flip": lambda: runDraftCommand("Draft_FlipDimension"),
    "help": ayuda,
}

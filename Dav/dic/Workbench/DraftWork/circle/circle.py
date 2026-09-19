import FreeCAD as App

try:
    from createobjects import CreateObjects
except ImportError:
    from selection.createobjects import CreateObjects
from ..draftcommand import runDraftCommand
from .ayuda import ayuda

def center():
    runDraftCommand("Draft_Circle")

    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()

circle = {
    "center": center,
    "help": ayuda,
}

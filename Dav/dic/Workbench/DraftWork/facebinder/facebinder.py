import FreeCAD as App

try:
    from createobjects import CreateObjects
except ImportError:
    from selection.createobjects import CreateObjects
from ..draftcommand import runDraftCommand
from .. import _modify
from .ayuda import ayuda


def create():
    runDraftCommand("Draft_Facebinder")
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


facebinder = {
    "create": _modify.facebinder,
    "help": ayuda,
    "interactive": create,
}

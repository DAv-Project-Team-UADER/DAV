import FreeCAD as App

try:
    from createobjects import CreateObjects
except ImportError:
    from selection.createobjects import CreateObjects
from ..draftcommand import runDraftCommand
from .ayuda import ayuda


def clone():
    runDraftCommand("Draft_Clone")
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def sketch():
    runDraftCommand("Draft_Draft2Sketch")
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def offset():
    runDraftCommand("Draft_Offset")
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


modify = {
    "clone": clone,
    "downgrade": lambda: runDraftCommand("Draft_Downgrade"),
    "sketch": sketch,
    "edit": lambda: runDraftCommand("Draft_Edit"),
    "fillet": lambda: runDraftCommand("Draft_Fillet"),
    "join": lambda: runDraftCommand("Draft_Join"),
    "move": lambda: runDraftCommand("Draft_Move"),
    "offset": offset,
    "rotate": lambda: runDraftCommand("Draft_Rotate"),
    "mirror": lambda: runDraftCommand("Draft_Mirror"),
    "help": ayuda,
}

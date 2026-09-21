import FreeCAD as App

try:
    from createobjects import CreateObjects
except ImportError:
    from selection.createobjects import CreateObjects
from ..draftcommand import runDraftCommand
from .. import _modify
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
    "clone": _modify.clone,
    "downgrade": _modify.downgrade,
    "sketch": _modify.to_sketch,
    "edit": _modify.edit_point,
    "fillet": _modify.fillet,
    "join": _modify.join,
    "move": _modify.move,
    "offset": _modify.offset,
    "rotate": _modify.rotate,
    "mirror": _modify.mirror,
    "help": ayuda,
    "interactive_clone": clone,
    "interactive_sketch": sketch,
    "interactive_offset": offset,
    "interactive_downgrade": lambda: runDraftCommand("Draft_Downgrade"),
    "interactive_edit": lambda: runDraftCommand("Draft_Edit"),
    "interactive_fillet": lambda: runDraftCommand("Draft_Fillet"),
    "interactive_join": lambda: runDraftCommand("Draft_Join"),
    "interactive_move": lambda: runDraftCommand("Draft_Move"),
    "interactive_rotate": lambda: runDraftCommand("Draft_Rotate"),
    "interactive_mirror": lambda: runDraftCommand("Draft_Mirror"),
}

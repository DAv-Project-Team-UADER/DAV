import FreeCAD as App

try:
    from createobjects import CreateObjects
except ImportError:
    from selection.createobjects import CreateObjects
from ..draftcommand import runDraftCommand
from ..._text import voiceShapeString
from .ayuda import ayuda


def text():
    runDraftCommand("Draft_Text")
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def shapestring():
    runDraftCommand("Draft_ShapeString")
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def label():
    runDraftCommand("Draft_Label")
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


annotation = {
    "text": voiceShapeString,
    "interactive_text": text,
    "shapestring": shapestring,
    "label": label,
    "help": ayuda,
}

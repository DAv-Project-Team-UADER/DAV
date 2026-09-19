import FreeCAD as App
from ..draftcommand import runDraftCommand
from .ayuda import ayuda
from selection.createobjects import CreateObjects


def circular():
    runDraftCommand("Draft_CircularArray")
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def ortho():
    runDraftCommand("Draft_OrthoArray")
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def polar():
    runDraftCommand("Draft_PolarArray")
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def path():
    runDraftCommand("Draft_PathArray")
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def pathlink():
    runDraftCommand("Draft_PathLinkArray")
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def point():
    runDraftCommand("Draft_PointArray")
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def pointlink():
    runDraftCommand("Draft_PointLinkArray")
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


array = {
    'circular': circular,
    'ortho': ortho,
    'polar': polar,
    'path': path,
    'pathlink': pathlink,
    'point': point,
    'pointlink': pointlink,
    'help': ayuda
}
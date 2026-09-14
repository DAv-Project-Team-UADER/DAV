import FreeCAD as App
import FreeCADGui as Gui
from .ayuda import ayuda
from selection.createobjects import CreateObjects


def circular():
    Gui.runCommand('Draft_CircularArray', 0)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def ortho():
    Gui.runCommand('Draft_OrthoArray', 0)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def polar():
    Gui.runCommand('Draft_PolarArray', 0)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def path():
    Gui.runCommand('Draft_PathArray', 0)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def pathlink():
    Gui.runCommand('Draft_PathLinkArray', 0)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def point():
    Gui.runCommand('Draft_PointArray', 0)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def pointlink():
    Gui.runCommand('Draft_PointLinkArray', 0)
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
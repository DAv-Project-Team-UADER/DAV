import FreeCAD as App
from ..draftcommand import runDraftCommand
from .. import _modify
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
    "circular": _modify.circular_array,
    "ortho": _modify.ortho_array,
    "polar": _modify.polar_array,
    "path": _modify.path_array,
    "pathlink": _modify.path_link_array,
    "point": _modify.point_array,
    "pointlink": _modify.point_link_array,
    "help": ayuda,
    "interactive_circular": circular,
    "interactive_ortho": ortho,
    "interactive_polar": polar,
    "interactive_path": path,
    "interactive_pathlink": pathlink,
    "interactive_point": point,
    "interactive_pointlink": pointlink,
}

import FreeCAD as App

try:
    from createobjects import CreateObjects
except ImportError:
    from selection.createobjects import CreateObjects
from ..draftcommand import runDraftCommand
from .ayuda import ayuda


def shape_2d_view():
    runDraftCommand("Draft_Shape2DView")
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def wire_to_bspline():
    runDraftCommand("Draft_WireToBSpline")
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


modification = {
    "scale": lambda: runDraftCommand("Draft_Scale"),
    "shape_2d_view": shape_2d_view,
    "slope": lambda: runDraftCommand("Draft_Slope"),
    "split": lambda: runDraftCommand("Draft_Split"),
    "stretch": lambda: runDraftCommand("Draft_Stretch"),
    "subelement_highlight": lambda: runDraftCommand("Draft_SubelementHighlight"),
    "trimex": lambda: runDraftCommand("Draft_Trimex"),
    "upgrade": lambda: runDraftCommand("Draft_Upgrade"),
    "wire_to_bspline": wire_to_bspline,
    "help": ayuda,
}

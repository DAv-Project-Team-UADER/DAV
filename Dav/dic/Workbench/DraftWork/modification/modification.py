import FreeCAD as App

try:
    from createobjects import CreateObjects
except ImportError:
    from selection.createobjects import CreateObjects
from ..draftcommand import runDraftCommand
from .. import _modify
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
    "scale": _modify.scale,
    "shape_2d_view": _modify.shape_2d_view,
    "slope": _modify.slope,
    "split": _modify.split_wire,
    "stretch": _modify.stretch,
    "subelement_highlight": _modify.highlight_subelements,
    "trimex": _modify.trim_extend,
    "upgrade": _modify.upgrade,
    "wire_to_bspline": _modify.wire_to_bspline,
    "help": ayuda,
    "interactive_scale": lambda: runDraftCommand("Draft_Scale"),
    "interactive_slope": lambda: runDraftCommand("Draft_Slope"),
    "interactive_split": lambda: runDraftCommand("Draft_Split"),
    "interactive_stretch": lambda: runDraftCommand("Draft_Stretch"),
    "interactive_trimex": lambda: runDraftCommand("Draft_Trimex"),
    "interactive_upgrade": lambda: runDraftCommand("Draft_Upgrade"),
}

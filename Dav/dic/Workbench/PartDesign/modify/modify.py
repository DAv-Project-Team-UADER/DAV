import FreeCAD as App
import FreeCADGui as Gui
from .ayuda import ayuda
from ._parametric import (
    chamfer_by_size,
    chamfer_by_size_and_angle,
    fillet_by_radius,
    thickness_by_value,
)


def _execute_with_objects(command_name: str, is_3d: bool = True) -> None:
    try:
        Gui.activateWorkbench("PartDesignWorkbench")
    except Exception:
        pass
    Gui.runCommand(command_name, 0)
    active_doc = App.ActiveDocument
    if not active_doc or not getattr(active_doc, 'ActiveObject', None):
        return
    obj_name = active_doc.ActiveObject.Name
    try:
        from createobjects import CreateObjects
    except ImportError:
        try:
            from selection.createobjects import CreateObjects
        except ImportError:
            from Dav.scr.selection.createobjects import CreateObjects
    CreateObjects(ObjectName=obj_name, Is3D=is_3d).Execute()


def chamfer() -> None:
    _execute_with_objects('PartDesign_Chamfer', is_3d=True)


modify = {
    'fillet':    lambda: Gui.runCommand('PartDesign_Fillet', 0),
    'chamfer':   chamfer,
    'draft':     lambda: Gui.runCommand('PartDesign_Draft', 0),
    'thickness': lambda: Gui.runCommand('PartDesign_Thickness', 0),
    'fillet_by_radius':          fillet_by_radius,
    'chamfer_by_size':           chamfer_by_size,
    'chamfer_by_size_and_angle': chamfer_by_size_and_angle,
    'thickness_by_value':        thickness_by_value,
    'help':      ayuda,
}

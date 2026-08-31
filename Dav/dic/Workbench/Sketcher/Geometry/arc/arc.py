# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)

import FreeCAD as App
import FreeCADGui as Gui
from .ayuda import ayuda
from ._parametric import create_by_center
from selection.createobjects import CreateObjects

def _execute_with_objects(command):
    Gui.runCommand(command, 0)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def create_by_center_with_objects(x: float, y: float, radius: float, angle_start: float, angle_end: float, label: str = "Arc"):
    create_by_center(x=x, y=y, radius=radius, angle_start=angle_start, angle_end=angle_end, label=label)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()

arc = {
    'center': lambda: _execute_with_objects('Sketcher_CreateArc'),
    '3point': lambda: _execute_with_objects('Sketcher_Create3PointArc'),
    'create_by_center': create_by_center_with_objects,
    'help':   ayuda
}
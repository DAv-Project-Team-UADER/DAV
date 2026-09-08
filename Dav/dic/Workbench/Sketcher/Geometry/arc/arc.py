# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)

import FreeCAD as App
import FreeCADGui as Gui
from .ayuda import ayuda
from ._parametric import create_by_center, create_by_3points
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


def create_by_3points_with_objects(x1: float, y1: float, x2: float, y2: float, x3: float, y3: float, label: str = "Arc"):
    create_by_3points(x1=x1, y1=y1, x2=x2, y2=y2, x3=x3, y3=y3, label=label)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()

arc = {
    'center': lambda: _execute_with_objects('Sketcher_CreateArc'),
    '3point': lambda: _execute_with_objects('Sketcher_Create3PointArc'),
    'create_by_center': create_by_center_with_objects,
    'create_by_3points': create_by_3points_with_objects,
    'help':   ayuda
}
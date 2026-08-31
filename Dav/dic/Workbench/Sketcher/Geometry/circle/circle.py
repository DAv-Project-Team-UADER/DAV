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


def create_by_center_with_objects(x: float, y: float, radius: float, label: str = "Circle"):
    create_by_center(x=x, y=y, radius=radius, label=label)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()

circle = {
    'create': lambda: _execute_with_objects('Sketcher_CreateCircle'),
    '3point': lambda: _execute_with_objects('Sketcher_Create3PointCircle'),
    'create_by_center': create_by_center_with_objects,
    'help':   ayuda
}
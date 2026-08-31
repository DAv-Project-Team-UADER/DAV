# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)

import FreeCAD as App
import FreeCADGui as Gui
from .ayuda import ayuda
from ._parametric import create_by_corners
from selection.createobjects import CreateObjects

def _execute_with_objects(command):
    Gui.runCommand(command, 0)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def create_by_corners_with_objects(x1: float, y1: float, x2: float, y2: float, label: str = "Rectangle"):
    create_by_corners(x1=x1, y1=y1, x2=x2, y2=y2, label=label)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()

rectangle = {
    'create': lambda: _execute_with_objects('Sketcher_CreateRectangle'),
    'center': lambda: _execute_with_objects('Sketcher_CreateRectangle_Center'),
    'create_by_corners': create_by_corners_with_objects,
    'help':   ayuda
}
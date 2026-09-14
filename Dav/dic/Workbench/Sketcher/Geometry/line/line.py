# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)

import FreeCAD as App
import FreeCADGui as Gui
from .ayuda import ayuda
from ._parametric import create_by_points
from selection.createobjects import CreateObjects

def create_line_with_objects():
    Gui.runCommand('Sketcher_CreateLine', 0)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()

def create_by_points_with_objects(x1: float, y1: float, x2: float, y2: float, label: str = "Segment"):
    create_by_points(x1=x1, y1=y1, x2=x2, y2=y2, label=label)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()

line = {
    'create': create_line_with_objects,
    'create_by_points': create_by_points_with_objects,
    'help':   ayuda
}
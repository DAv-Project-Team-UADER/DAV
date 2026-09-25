# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)

import FreeCAD as App
import FreeCADGui as Gui
from .ayuda import ayuda
from ._parametric import create_by_center, create_by_corners
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

def create_by_center_with_objects(x: float, y: float, width: float, height: float, label: str = "Rectangle"):
    create_by_center(x=x, y=y, width=width, height=height, label=label)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


rectangle = {
    # 'create' y 'center' son paramétricos con ventana (igual que circle.create):
    # cada float dispara un InputPrompt via ParameterCollector, no la herramienta
    # del mouse de Sketcher.
    'create': create_by_corners_with_objects,
    'center': create_by_center_with_objects,
    'create_by_corners': create_by_corners_with_objects,
    'create_by_center': create_by_center_with_objects,
    # modo interactivo legacy por si se necesita mouse (no usado por voz pura)
    'interactive': lambda: _execute_with_objects('Sketcher_CreateRectangle'),
    'interactive_center': lambda: _execute_with_objects('Sketcher_CreateRectangle_Center'),
    'help':   ayuda
}
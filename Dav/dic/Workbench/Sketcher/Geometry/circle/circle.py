# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)

import FreeCAD as App
import FreeCADGui as Gui
from .ayuda import ayuda
from ._parametric import create_by_center, create_by_3_points
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


def create_by_3_points_with_objects(
    x1: float, y1: float, x2: float, y2: float, x3: float, y3: float, label: str = "Circle3P"
):
    create_by_3_points(x1=x1, y1=y1, x2=x2, y2=y2, x3=x3, y3=y3, label=label)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()

circle = {
    # 'create' y '3point' ahora son paramétricos con ventana (igual que
    # line.create_by_points). Cada float dispara un InputPrompt via
    # ParameterCollector/Validator, no el comando interactivo que solo dejaba puntos sueltos.
    'create': create_by_center_with_objects,
    '3point': create_by_3_points_with_objects,
    # alias explícitos para voz: "círculo por centro" / "círculo por 3 puntos"
    'create_by_center': create_by_center_with_objects,
    'create_by_3_points': create_by_3_points_with_objects,
    # modo interactivo legacy por si se necesita mouse (no usado por voz pura)
    'interactive': lambda: _execute_with_objects('Sketcher_CreateCircle'),
    'interactive_3point': lambda: _execute_with_objects('Sketcher_Create3PointCircle'),
    'help':   ayuda
}
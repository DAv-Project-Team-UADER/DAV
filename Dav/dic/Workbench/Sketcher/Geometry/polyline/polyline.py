# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)

import FreeCAD as App
import FreeCADGui as Gui
from .ayuda import ayuda
from selection.createobjects import CreateObjects

def _execute_with_objects():
    Gui.runCommand('Sketcher_CreatePolyline', 0)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()

polyline = {
    'create': _execute_with_objects,
    'help':   ayuda
}
# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)

import FreeCAD as App
import FreeCADGui as Gui
from .ayuda import ayuda
from selection.createobjects import CreateObjects

def _execute_with_objects(command):
    Gui.runCommand(command, 0)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()

ellipse = {
    'center':     lambda: _execute_with_objects('Sketcher_CreateEllipseByCenter'),
    '3points':    lambda: _execute_with_objects('Sketcher_CreateEllipseBy3Points'),
    'elliptic':   lambda: _execute_with_objects('Sketcher_CreateArcOfEllipse'),
    'hyperbolic': lambda: _execute_with_objects('Sketcher_CreateArcOfHyperbola'),
    'parabolic':  lambda: _execute_with_objects('Sketcher_CreateArcOfParabola'),
    'help':       ayuda,
}
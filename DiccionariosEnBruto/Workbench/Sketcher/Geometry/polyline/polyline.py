import FreeCADGui as Gui
from .ayuda import ayuda

polyline = {
    'create': lambda: Gui.runCommand('Sketcher_CreatePolyline', 0),
    'help':   ayuda
}
import FreeCADGui as Gui
from .ayuda import ayuda

circle = {
    'create': lambda: Gui.runCommand('Sketcher_CreateCircle', 0),
    '3point': lambda: Gui.runCommand('Sketcher_Create3PointCircle', 0),
    'help':   ayuda
}
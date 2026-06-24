import FreeCADGui as Gui
from .ayuda import ayuda

arc = {
    'center': lambda: Gui.runCommand('Sketcher_CreateArc', 0),
    '3point': lambda: Gui.runCommand('Sketcher_Create3PointArc', 0),
    'help':   ayuda
}
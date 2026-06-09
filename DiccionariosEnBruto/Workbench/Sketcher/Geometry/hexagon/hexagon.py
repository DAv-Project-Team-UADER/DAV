import FreeCADGui as Gui
from .ayuda import ayuda

hexagon = {
    'create': lambda: Gui.runCommand('Sketcher_CreateHexagon', 0),
    'help':   ayuda
}
import FreeCADGui as Gui
from .ayuda import ayuda

point = {
    'create': lambda: Gui.runCommand('Sketcher_CreatePoint', 0),
    'help':   ayuda
}
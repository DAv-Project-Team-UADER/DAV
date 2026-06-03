import FreeCADGui as Gui
from .ayuda import ayuda

square = {
    'create': lambda: Gui.runCommand('Sketcher_CreateSquare', 0),
    'help':   ayuda
}
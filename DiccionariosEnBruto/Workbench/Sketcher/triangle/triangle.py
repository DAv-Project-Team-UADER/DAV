import FreeCADGui as Gui
from .ayuda import ayuda

triangle = {
    'create': lambda: Gui.runCommand('Sketcher_CreateTriangle', 0),
    'help':   ayuda
}
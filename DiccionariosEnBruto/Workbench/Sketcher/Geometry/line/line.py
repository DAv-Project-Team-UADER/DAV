import FreeCADGui as Gui
from .ayuda import ayuda

line = {
    'create': lambda: Gui.runCommand('Sketcher_CreateLine', 0),
    'help':   ayuda
}
import FreeCADGui as Gui
from .ayuda import ayuda

heptagon = {
    'create': lambda: Gui.runCommand('Sketcher_CreateHeptagon', 0),
    'help':   ayuda
}
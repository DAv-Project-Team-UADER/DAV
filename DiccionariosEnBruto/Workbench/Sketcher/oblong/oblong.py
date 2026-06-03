import FreeCADGui as Gui
from .ayuda import ayuda

oblong = {
    'create': lambda: Gui.runCommand('Sketcher_CreateSlot', 0),
    'help':   ayuda
}
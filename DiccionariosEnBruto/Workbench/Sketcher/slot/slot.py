import FreeCADGui as Gui
from .ayuda import ayuda

slot = {
    'create': lambda: Gui.runCommand('Sketcher_CreateSlot', 0),
    'help':   ayuda
}
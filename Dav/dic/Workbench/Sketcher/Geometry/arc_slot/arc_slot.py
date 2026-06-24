import FreeCADGui as Gui
from .ayuda import ayuda

arc_slot = {
    'arc_ends':  lambda: Gui.runCommand('Sketcher_CreateArcSlot', 0),
    'flat_ends': lambda: Gui.runCommand('Sketcher_CreateArcSlot', 0),
    'help':      ayuda
}
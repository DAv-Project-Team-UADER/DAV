import FreeCADGui as Gui
from .ayuda import ayuda

arc_slot = {
    'arcends':  lambda: Gui.runCommand('Sketcher_CreateArcSlot', 0),
    'flatends': lambda: Gui.runCommand('Sketcher_CreateArcSlot', 0),
    'help':     ayuda,
}
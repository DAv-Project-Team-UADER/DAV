import FreeCADGui as Gui
from .ayuda import ayuda

rectangle = {
    'create': lambda: Gui.runCommand('Sketcher_CreateRectangle', 0),
    'center': lambda: Gui.runCommand('Sketcher_CreateRectangle_Center', 0),
    'help':   ayuda
}
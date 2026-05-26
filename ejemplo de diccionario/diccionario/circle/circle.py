import FreeCADGui as Gui
from .ayuda import ayuda

circle = {
    'center': lambda: Gui.runCommand('Draft_Circle', 0),
    'help':   ayuda
}
import FreeCADGui as Gui
from .ayuda import ayuda

arc = {
    'center': lambda: Gui.runCommand('Draft_Arc', 0),
    'points': lambda: Gui.runCommand('Draft_Arc_3Points', 0),
    'help':   ayuda
}
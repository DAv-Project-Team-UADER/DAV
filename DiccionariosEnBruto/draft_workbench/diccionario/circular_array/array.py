import FreeCADGui as Gui
from .ayuda import ayuda

array = {
    'circular': lambda: Gui.runCommand('Draft_CircularArray', 0),
    'help':     ayuda
}
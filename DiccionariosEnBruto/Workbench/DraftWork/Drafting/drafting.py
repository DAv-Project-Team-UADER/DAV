import FreeCADGui as Gui
from .ayuda import ayuda

drafting = {
    'wire': lambda: Gui.runCommand('Draft_Wire', 0),
    'help': ayuda
}
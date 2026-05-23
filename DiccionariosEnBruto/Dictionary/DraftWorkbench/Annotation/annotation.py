import FreeCADGui as Gui
from .ayuda import ayuda

annotation = {
    'text': lambda: Gui.runCommand('Draft_Text', 0),
    'shape_string': lambda: Gui.runCommand('Draft_ShapeString', 0),
    'help': ayuda
}
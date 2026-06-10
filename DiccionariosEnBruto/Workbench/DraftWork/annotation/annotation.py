import FreeCADGui as Gui
from .ayuda import ayuda

annotation = {
    'text':         lambda: Gui.runCommand('Draft_Text', 0),
    'shapestring': lambda: Gui.runCommand('Draft_ShapeString', 0),
    'label':        lambda: Gui.runCommand('Draft_Label', 0),
    'help':         ayuda,
}
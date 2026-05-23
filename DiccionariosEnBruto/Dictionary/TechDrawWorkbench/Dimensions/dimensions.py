import FreeCADGui as Gui
from .ayuda import ayuda

dimensions = {
    'vertical': lambda: Gui.runCommand('TechDraw_VerticalDimension', 0),
    'help': ayuda
}
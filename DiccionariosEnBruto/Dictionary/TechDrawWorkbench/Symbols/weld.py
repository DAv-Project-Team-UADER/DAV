import FreeCADGui as Gui
from .ayuda import ayuda

symbols = {
    'weld_symbol': lambda: Gui.runCommand('TechDraw_WeldSymbol', 0),
    'help': ayuda
}
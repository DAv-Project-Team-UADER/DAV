import FreeCADGui as Gui
from .ayuda import ayuda

views = {
    'view': lambda: Gui.runCommand('TechDraw_View', 0),
    'help': ayuda
}
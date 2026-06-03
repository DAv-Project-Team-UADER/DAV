import FreeCADGui as Gui
from .ayuda import ayuda

add_vertices = {
    'cosmetic': lambda: Gui.runCommand('TechDraw_CosmeticVertex', 0),
    'help': ayuda
}
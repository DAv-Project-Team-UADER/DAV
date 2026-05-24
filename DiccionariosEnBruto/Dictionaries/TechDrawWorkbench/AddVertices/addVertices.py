import FreeCADGui as Gui
from .help import help

add_vertices = {
    'cosmetic': lambda: Gui.runCommand('TechDraw_CosmeticVertex', 0),
    'help': help
}
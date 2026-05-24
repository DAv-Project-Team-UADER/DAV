import FreeCADGui as Gui
from .help import help

add_lines = {
    'face_center': lambda: Gui.runCommand('TechDraw_FaceCenterLine', 0),
    'decorate': lambda: Gui.runCommand('TechDraw_DecorateLine', 0),
    'help': help
}
import FreeCADGui as Gui
from .ayuda import ayuda

centerlines = {
    'two_lines': lambda: Gui.runCommand('TechDraw_2LineCenterLine', 0),
    'two_points': lambda: Gui.runCommand('TechDraw_2PointCenterLine', 0),
    'help': ayuda
}
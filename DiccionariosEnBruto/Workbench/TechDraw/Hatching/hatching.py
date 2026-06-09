import FreeCADGui as Gui
from .ayuda import ayuda

hatching = {
    'geometric_hatch': lambda: Gui.runCommand('TechDraw_GeometricHatch', 0),
    'help': ayuda
}
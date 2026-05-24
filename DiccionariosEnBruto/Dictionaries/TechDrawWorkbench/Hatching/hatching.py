import FreeCADGui as Gui
from .help import help

hatching = {
    'geometric_hatch': lambda: Gui.runCommand('TechDraw_GeometricHatch', 0),
    'help': help
}
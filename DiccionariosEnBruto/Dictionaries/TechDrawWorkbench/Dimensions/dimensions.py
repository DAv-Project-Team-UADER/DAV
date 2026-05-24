import FreeCADGui as Gui
from .help import help

dimensions = {
    'angle': lambda: Gui.runCommand('TechDraw_AngleDimension', 0),
    '3pt_angle': lambda: Gui.runCommand('TechDraw_3PtAngleDimension', 0),
    'area': lambda: Gui.runCommand('TechDraw_AreaDimension', 0),
    'diameter': lambda: Gui.runCommand('TechDraw_DiameterDimension', 0),
    'dimension': lambda: Gui.runCommand('TechDraw_Dimension', 0),
    'help': help
}
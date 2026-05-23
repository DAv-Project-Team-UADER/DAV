import FreeCADGui as Gui
from .ayuda import ayuda

# Diccionario de la categoría Modification
modification = {
    'scale': lambda: Gui.runCommand('Draft_Scale', 0),
    'shape_2d_view': lambda: Gui.runCommand('Draft_Shape2DView', 0),
    'slope': lambda: Gui.runCommand('Draft_Slope', 0),
    'split': lambda: Gui.runCommand('Draft_Split', 0),
    'stretch': lambda: Gui.runCommand('Draft_Stretch', 0),
    'subelement_highlight': lambda: Gui.runCommand('Draft_SubelementHighlight', 0),
    'trimex': lambda: Gui.runCommand('Draft_Trimex', 0),
    'upgrade': lambda: Gui.runCommand('Draft_Upgrade', 0),
    'wire_to_bspline': lambda: Gui.runCommand('Draft_WireToBSpline', 0),
    'help': ayuda
}
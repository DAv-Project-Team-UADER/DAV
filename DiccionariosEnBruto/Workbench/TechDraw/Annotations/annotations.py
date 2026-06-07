import FreeCADGui as Gui
from .ayuda import ayuda

annotations = {
    'annotation': lambda: Gui.runCommand('TechDraw_Annotation', 0),
    'axo_length': lambda: Gui.runCommand('TechDraw_AxoLengthDimension', 0),
    'balloon': lambda: Gui.runCommand('TechDraw_Balloon', 0),
    'help': ayuda
}
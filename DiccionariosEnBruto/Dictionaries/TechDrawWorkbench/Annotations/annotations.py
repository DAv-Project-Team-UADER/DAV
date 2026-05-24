import FreeCADGui as Gui
from .help import help

annotations = {
    'annotation': lambda: Gui.runCommand('TechDraw_Annotation', 0),
    'axo_length': lambda: Gui.runCommand('TechDraw_AxoLengthDimension', 0),
    'balloon': lambda: Gui.runCommand('TechDraw_Balloon', 0),
    'help': help
}
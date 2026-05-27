import FreeCADGui as Gui
from .ayuda import ayuda

ellipse = {
    'center': lambda: Gui.runCommand('Draft_Ellipse', 0),
    'help':   ayuda
}
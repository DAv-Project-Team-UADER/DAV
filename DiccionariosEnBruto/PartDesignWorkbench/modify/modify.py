import FreeCADGui as Gui
from .ayuda import ayuda

modify = {
    'fillet':    lambda: Gui.runCommand('PartDesign_Fillet', 0),
    'chamfer':   lambda: Gui.runCommand('PartDesign_Chamfer', 0),
    'draft':     lambda: Gui.runCommand('PartDesign_Draft', 0),
    'thickness': lambda: Gui.runCommand('PartDesign_Thickness', 0),
    'boolean':   lambda: Gui.runCommand('PartDesign_Boolean', 0),
    'help':      ayuda,
}

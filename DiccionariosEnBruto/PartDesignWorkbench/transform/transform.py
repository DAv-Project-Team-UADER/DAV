import FreeCADGui as Gui
from .ayuda import ayuda

transform = {
    'linearpattern':  lambda: Gui.runCommand('PartDesign_LinearPattern', 0),
    'mirrored':       lambda: Gui.runCommand('PartDesign_Mirrored', 0),
    'polarpattern':   lambda: Gui.runCommand('PartDesign_PolarPattern', 0),
    'multitransform': lambda: Gui.runCommand('PartDesign_MultiTransform', 0),
    'scaled':         lambda: Gui.runCommand('PartDesign_MultiTransform', 0),
    'help':           ayuda,
}

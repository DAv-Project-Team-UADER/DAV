import FreeCADGui as Gui
from .ayuda import ayuda

additive = {
    'pad':               lambda: Gui.runCommand('PartDesign_Pad', 0),
    'revolution':        lambda: Gui.runCommand('PartDesign_Revolution', 0),
    'additivehelix':     lambda: Gui.runCommand('PartDesign_AdditiveHelix', 0),
    'additiveloft':      lambda: Gui.runCommand('PartDesign_AdditiveLoft', 0),
    'additivepipe':      lambda: Gui.runCommand('PartDesign_AdditivePipe', 0),
    'additivebox':       lambda: Gui.runCommand('PartDesign_AdditiveBox', 0),
    'additivecone':      lambda: Gui.runCommand('PartDesign_AdditiveCone', 0),
    'additivecylinder':  lambda: Gui.runCommand('PartDesign_AdditiveCylinder', 0),
    'additiveellipsoid': lambda: Gui.runCommand('PartDesign_AdditiveEllipsoid', 0),
    'additiveprism':     lambda: Gui.runCommand('PartDesign_AdditivePrism', 0),
    'additivesphere':    lambda: Gui.runCommand('PartDesign_AdditiveSphere', 0),
    'additivetorus':     lambda: Gui.runCommand('PartDesign_AdditiveTorus', 0),
    'additivewedge':     lambda: Gui.runCommand('PartDesign_AdditiveWedge', 0),
    'help':              ayuda,
}

import FreeCADGui as Gui
from .ayuda import ayuda

subtractive = {
    'pocket':               lambda: Gui.runCommand('PartDesign_Pocket', 0),
    'groove':               lambda: Gui.runCommand('PartDesign_Groove', 0),
    'hole':                 lambda: Gui.runCommand('PartDesign_Hole', 0),
    'subtractivebox':       lambda: Gui.runCommand('PartDesign_SubtractiveBox', 0),
    'subtractivecone':      lambda: Gui.runCommand('PartDesign_SubtractiveCone', 0),
    'subtractivecylinder':  lambda: Gui.runCommand('PartDesign_SubtractiveCylinder', 0),
    'subtractiveellipsoid': lambda: Gui.runCommand('PartDesign_SubtractiveEllipsoid', 0),
    'subtractivehelix':     lambda: Gui.runCommand('PartDesign_SubtractiveHelix', 0),
    'subtractiveloft':      lambda: Gui.runCommand('PartDesign_SubtractiveLoft', 0),
    'subtractivepipe':      lambda: Gui.runCommand('PartDesign_SubtractivePipe', 0),
    'subtractiveprism':     lambda: Gui.runCommand('PartDesign_SubtractivePrism', 0),
    'subtractivesphere':    lambda: Gui.runCommand('PartDesign_SubtractiveSphere', 0),
    'subtractivetorus':     lambda: Gui.runCommand('PartDesign_SubtractiveTorus', 0),
    'subtractivewedge':     lambda: Gui.runCommand('PartDesign_SubtractiveWedge', 0),
    'boolean':              lambda: Gui.runCommand('PartDesign_Boolean', 0),
    'thickness':            lambda: Gui.runCommand('PartDesign_Thickness', 0),
    'wizardshaft':          lambda: Gui.runCommand('PartDesign_WizardShaft', 0),
    'help':                 ayuda,
}

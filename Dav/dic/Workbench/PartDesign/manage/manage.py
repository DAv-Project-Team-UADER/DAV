import FreeCADGui as Gui
from .ayuda import ayuda

manage = {
    'movefeature':       lambda: Gui.runCommand('PartDesign_MoveFeature', 0),
    'movefeatureintree': lambda: Gui.runCommand('PartDesign_MoveFeatureInTree', 0),
    'movetip':           lambda: Gui.runCommand('PartDesign_MoveTip', 0),
    'preferences':       lambda: Gui.runCommand('Std_DlgPreferences', 0),
    'wizardshaft':       lambda: Gui.runCommand('PartDesign_WizardShaft', 0),
    'help':              ayuda,
}

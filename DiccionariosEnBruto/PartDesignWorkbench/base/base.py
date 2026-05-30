import FreeCADGui as Gui
from .ayuda import ayuda

base = {
    'body':           lambda: Gui.runCommand('PartDesign_Body', 0),
    'newsketch':      lambda: Gui.runCommand('PartDesign_NewSketch', 0),
    'clone':          lambda: Gui.runCommand('PartDesign_Clone', 0),
    'subshapebinder': lambda: Gui.runCommand('PartDesign_SubShapeBinder', 0),
    'help':           ayuda,
}

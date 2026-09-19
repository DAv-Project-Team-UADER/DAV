import FreeCADGui as Gui
from .ayuda import ayuda
from .new_sketch import _new_sketch_partdesign

base = {
    'body':           lambda: Gui.runCommand('PartDesign_Body', 0),
    'newsketch':      _new_sketch_partdesign,
    'clone':          lambda: Gui.runCommand('PartDesign_Clone', 0),
    'subshapebinder': lambda: Gui.runCommand('PartDesign_SubShapeBinder', 0),
    'help':           ayuda,
}

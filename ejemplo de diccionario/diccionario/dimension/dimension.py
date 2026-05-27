import FreeCADGui as Gui
from .ayuda import ayuda

dimension = {
    "linear": lambda: Gui.runCommand("Draft_Dimension", 0),
    "flip": lambda: Gui.runCommand("Draft_FlipDimension", 0),
    "help": ayuda,
}

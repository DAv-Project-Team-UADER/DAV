import FreeCADGui as Gui
from .ayuda import ayuda

modify = {
    "clone": lambda: Gui.runCommand("Draft_Clone", 0),
    "downgrade": lambda: Gui.runCommand("Draft_Downgrade", 0),
    "sketch": lambda: Gui.runCommand("Draft_Draft2Sketch", 0),
    "edit": lambda: Gui.runCommand("Draft_Edit", 0),
    "fillet": lambda: Gui.runCommand("Draft_Fillet", 0),
    "help": ayuda,
}

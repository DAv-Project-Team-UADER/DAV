import FreeCADGui as Gui
from .ayuda import ayuda

modify = {
    "clone":    lambda: Gui.runCommand("Draft_Clone", 0),
    "downgrade": lambda: Gui.runCommand("Draft_Downgrade", 0),
    "sketch":   lambda: Gui.runCommand("Draft_Draft2Sketch", 0),
    "edit":     lambda: Gui.runCommand("Draft_Edit", 0),
    "fillet":   lambda: Gui.runCommand("Draft_Fillet", 0),
    "join":     lambda: Gui.runCommand("Draft_Join", 0),
    "move":     lambda: Gui.runCommand("Draft_Move", 0),
    "offset":   lambda: Gui.runCommand("Draft_Offset", 0),
    "rotate":   lambda: Gui.runCommand("Draft_Rotate", 0),
    "mirror":   lambda: Gui.runCommand("Draft_Mirror", 0),
    "help":     ayuda,
}

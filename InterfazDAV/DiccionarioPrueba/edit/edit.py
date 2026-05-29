import FreeCADGui as Gui
from .ayuda import ayuda

edit = {
    'undo':      lambda: Gui.runCommand('Std_Undo', 0),
    'redo':      lambda: Gui.runCommand('Std_Redo', 0),
    'copy':      lambda: Gui.runCommand('Std_Copy', 0),
    'cut':       lambda: Gui.runCommand('Std_Cut', 0),
    'paste':     lambda: Gui.runCommand('Std_Paste', 0),
    'delete':    lambda: Gui.runCommand('Std_Delete', 0),
    'selectall': lambda: Gui.runCommand('Std_SelectAll', 0),
    'help':      ayuda,
}

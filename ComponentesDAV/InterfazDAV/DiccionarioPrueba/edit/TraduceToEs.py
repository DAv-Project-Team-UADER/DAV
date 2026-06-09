


import ayuda
import FreeCADGui as Gui
TraduceToEs = {
    'deshacer':      lambda: Gui.runCommand('Std_Undo', 0),
    'rehacer':      lambda: Gui.runCommand('Std_Redo', 0),
    'copiar':      lambda: Gui.runCommand('Std_Copy', 0),
    'cortar':       lambda: Gui.runCommand('Std_Cut', 0),
    'pegar':     lambda: Gui.runCommand('Std_Paste', 0),
    'borrar':    lambda: Gui.runCommand('Std_Delete', 0),
    'seleccionar todo': lambda: Gui.runCommand('Std_SelectAll', 0),
    'ayuda':      ayuda,
}
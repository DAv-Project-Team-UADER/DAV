import FreeCADGui as Gui
from .ayuda import ayuda

file = {
    'new':    lambda: Gui.runCommand('Std_New', 0),
    'open':   lambda: Gui.runCommand('Std_Open', 0),
    'close':  lambda: Gui.runCommand('Std_CloseActiveWindow', 0),
    'save':   lambda: Gui.runCommand('Std_Save', 0),
    'saveas': lambda: Gui.runCommand('Std_SaveAs', 0),
    'help':   ayuda,
}

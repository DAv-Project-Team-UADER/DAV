import FreeCADGui as Gui
from .ayuda import ayuda

print_cmds = {
    'print': lambda: Gui.runCommand('Std_Print', 0),
    'pdf':   lambda: Gui.runCommand('Std_PrintPdf', 0),
    'help':  ayuda,
}

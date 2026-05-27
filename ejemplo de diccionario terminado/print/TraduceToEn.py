from print import print_cmds
from doc import doc
from ayuda import ayuda
import FreeCADGui as Gui
TraduceToEn = {
    'print': lambda: Gui.runCommand('Std_Print', 0),
    'normal': lambda: Gui.runCommand('Std_Print', 0),
    'paper': lambda: Gui.runCommand('Std_Print', 0),
    'pdf':   lambda: Gui.runCommand('Std_PrintPdf', 0),
    'Help': ayuda,
    'Assistance': ayuda,   # sinónimo adicional
}

#print_cmds = {
#    'print': lambda: Gui.runCommand('Std_Print', 0),
#    'pdf':   lambda: Gui.runCommand('Std_PrintPdf', 0),
#    'help':  ayuda,
#}

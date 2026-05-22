import FreeCADGui as Gui
from .ayuda import ayuda

facebinder = {
    'create': lambda: Gui.runCommand('Draft_Facebinder', 0),
    'help':   ayuda
}
import FreeCADGui as Gui
from .ayuda import ayuda

annotation = {
    'editor': lambda: Gui.runCommand('Draft_AnnotationStyleEditor', 0),
    'help': ayuda,
}
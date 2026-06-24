import FreeCADGui as Gui
from .ayuda import ayuda

array = {
    'circular': lambda: Gui.runCommand('Draft_CircularArray', 0),
    'ortho': lambda: Gui.runCommand('Draft_OrthoArray', 0),
    'polar': lambda: Gui.runCommand('Draft_PolarArray', 0),
    'path': lambda: Gui.runCommand('Draft_PathArray', 0),
    'pathlink': lambda: Gui.runCommand('Draft_PathLinkArray', 0),
    'point': lambda: Gui.runCommand('Draft_PointArray', 0),
    'pointlink': lambda: Gui.runCommand('Draft_PointLinkArray', 0),
    'help': ayuda
}
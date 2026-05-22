import FreeCAD as App
from .ayuda import ayuda


def _undo():
    App.ActiveDocument.undo()


def _redo():
    App.ActiveDocument.redo()


doc = {
    'undo': _undo,
    'redo': _redo,
    'help': ayuda,
}

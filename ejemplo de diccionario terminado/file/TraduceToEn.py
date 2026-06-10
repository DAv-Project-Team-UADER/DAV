import FreeCAD as App
import FreeCADGui as Gui
from .ayuda import ayuda


def _revert():
    doc = App.activeDocument()
    if doc and doc.FileName:
        name = doc.Name
        filename = doc.FileName
        App.closeDocument(name)
        App.open(filename)


TraduceToEn = {
    'new':    lambda: Gui.runCommand('Std_New', 0),
    'open':   lambda: Gui.runCommand('Std_Open', 0),
    'close':  lambda: Gui.runCommand('Std_CloseActiveWindow', 0),
    'save':   lambda: Gui.runCommand('Std_Save', 0),
    'saveas': lambda: Gui.runCommand('Std_SaveAs', 0),
    'quit': lambda: Gui.getMainWindow().close() if hasattr(Gui, 'getMainWindow') else Gui.runCommand('Std_Quit', 0),
    'exit': lambda: Gui.getMainWindow().close() if hasattr(Gui, 'getMainWindow') else Gui.runCommand('Std_Quit', 0),
    'revert': _revert,
    'recent files': lambda: Gui.runCommand('Std_RecentFiles', 0),
    'recent': lambda: Gui.runCommand('Std_RecentFiles', 0),
    'Help': ayuda,
    'Assistance': ayuda,   # sinónimo adicional
}

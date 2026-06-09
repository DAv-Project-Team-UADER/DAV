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


TraduceToPT = {
    'novo':    lambda: Gui.runCommand('Std_New', 0),
    'abrir':   lambda: Gui.runCommand('Std_Open', 0),
    'fechar':  lambda: Gui.runCommand('Std_CloseActiveWindow', 0),
    'salvar':   lambda: Gui.runCommand('Std_Save', 0),
    'salvar como': lambda: Gui.runCommand('Std_SaveAs', 0),
    'sair': lambda: Gui.getMainWindow().close() if hasattr(Gui, 'getMainWindow') else Gui.runCommand('Std_Quit', 0),
    'reverter': _revert,
    'recentes': lambda: Gui.runCommand('Std_RecentFiles', 0),
    'arquivos recentes': lambda: Gui.runCommand('Std_RecentFiles', 0),
    'ajuda': ayuda,
    'Assistência': ayuda,   # sinónimo adicional
}

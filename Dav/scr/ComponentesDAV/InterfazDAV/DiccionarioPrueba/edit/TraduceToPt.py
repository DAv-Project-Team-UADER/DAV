
from ayuda import ayuda
import FreeCADGui as Gui
TraduceToPtBr = {
     'desfazer':      lambda: Gui.runCommand('Std_Undo', 0),
    'refazer':       lambda: Gui.runCommand('Std_Redo', 0),
    'copiar':        lambda: Gui.runCommand('Std_Copy', 0),
    'cortar':        lambda: Gui.runCommand('Std_Cut', 0),
    'colar':         lambda: Gui.runCommand('Std_Paste', 0),
    'excluir':       lambda: Gui.runCommand('Std_Delete', 0),
    'selecionartudo': lambda: Gui.runCommand('Std_SelectAll', 0),
    'ajuda':         ayuda,
    'Ajuda':         ayuda,
    'Assistência':   ayuda,  # sinônimo adicional
}  # 

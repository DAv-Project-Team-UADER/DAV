from print import print_cmds
from doc import doc
from ayuda import ayuda
import FreeCADGui as Gui
TraduceToPtBr = {
    'Pasta': 'file',
    'Arquivo': 'file',
    'Folhas': 'file',      # sinónimo para 'Folios'
    'Páginas': 'file',     # sinónimo adicional
    'Editar': 'edit',
    'Edição': 'edit',      # sinónimo para 'edición'
    'Modificar': 'edit',   # sinónimo adicional
    'Imprimir': 'print_cmds',
    'Impressão': 'print_cmds',  # sinónimo para 'impresión'
    'Impressora': 'print_cmds', # sinónimo para 'impresora'
    'Atualizar': lambda: Gui.runCommand('Std_Refresh', 0),
    'Recarregar': lambda: Gui.runCommand('Std_Refresh', 0),   # sinónimo para 'recargar'
    'Refrescar': lambda: Gui.runCommand('Std_Refresh', 0),    # sinónimo para 'refrescar'
    'Foto': lambda: Gui.runCommand('Std_ViewScreenShot', 0),
    'Tirar foto': lambda: Gui.runCommand('Std_ViewScreenShot', 0),   # sinónimo para 'sacar foto'
    'Captura': lambda: Gui.runCommand('Std_ViewScreenShot', 0),      # sinónimo para 'captura'
    'Salvar tela': lambda: Gui.runCommand('Std_ViewScreenShot', 0),  # sinónimo para 'guardar pantalla'
    'Captura de tela': lambda: Gui.runCommand('Std_ViewScreenShot', 0), # sinónimo adicional
    'Documento de texto': lambda: Gui.runCommand('Std_TextDocument', 0),
    'Arquivo de texto': lambda: Gui.runCommand('Std_TextDocument', 0), # sinónimo adicional
    'Ajuda': ayuda,
    'Assistência': ayuda,  # sinónimo adicional
}
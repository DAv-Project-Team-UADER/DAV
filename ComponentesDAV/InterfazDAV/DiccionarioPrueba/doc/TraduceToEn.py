from print import print_cmds
from doc import doc
from ayuda import ayuda
import FreeCADGui as Gui
TraduceToEnUs = {
    'Folder': 'file',
    'File': 'file',
    'Sheets': 'file',      # sinónimo para 'Folios'
    'Documents': 'file',   # sinónimo adicional
    'Edit': 'edit',
    'Editing': 'edit',     # sinónimo para 'edición'
    'Modify': 'edit',      # sinónimo adicional
    'Print': 'print_cmds',
    'Printing': 'print_cmds',  # sinónimo para 'impresión'
    'Printer': 'print_cmds',   # sinónimo para 'impresora'
    'Refresh': lambda: Gui.runCommand('Std_Refresh', 0),
    'Reload': lambda: Gui.runCommand('Std_Refresh', 0),    # sinónimo para 'recargar'
    'Update': lambda: Gui.runCommand('Std_Refresh', 0),    # sinónimo para 'actualizar'
    'Photo': lambda: Gui.runCommand('Std_ViewScreenShot', 0),
    'Take photo': lambda: Gui.runCommand('Std_ViewScreenShot', 0),  # sinónimo para 'sacar foto'
    'Capture': lambda: Gui.runCommand('Std_ViewScreenShot', 0),      # sinónimo para 'captura'
    'Save screen': lambda: Gui.runCommand('Std_ViewScreenShot', 0),  # sinónimo para 'guardar pantalla'
    'Screenshot': lambda: Gui.runCommand('Std_ViewScreenShot', 0),   # sinónimo adicional
    'Screen capture': lambda: Gui.runCommand('Std_ViewScreenShot', 0),# sinónimo adicional
    'Text document': lambda: Gui.runCommand('Std_TextDocument', 0),
    'Text file': lambda: Gui.runCommand('Std_TextDocument', 0),      # sinónimo adicional
    'Document': lambda: Gui.runCommand('Std_TextDocument', 0),       # sinónimo adicional
    'Help': ayuda,
    'Assistance': ayuda,   # sinónimo adicional
}


from file import file
from edit import edit
from print import print_cmds
from doc import doc
from ayuda import ayuda
import FreeCADGui as Gui

TraduceToEs = {
    'Carpeta':  file,
    'Archivo':  file, #sinonimo
    'Folios':  file,  #sinonimo
    'editar': edit,
    'edición': edit, #sinonimo
    'imprimir': print_cmds,
    'impresión': print_cmds, #sinonimo
    'impresora': print_cmds, #sinonimo
    'refrescar':    lambda: Gui.runCommand('Std_Refresh', 0),
    'recargar':    lambda: Gui.runCommand('Std_Refresh', 0),#sinonimo
    'actualizar':    lambda: Gui.runCommand('Std_Refresh', 0),#sinonimo
    'foto': lambda: Gui.runCommand('Std_ViewScreenShot', 0),
    'sacar foto': lambda: Gui.runCommand('Std_ViewScreenShot', 0),#sinonimo
    'captura': lambda: Gui.runCommand('Std_ViewScreenShot', 0), #sinonimo
    'guardar pantalla': lambda: Gui.runCommand('Std_ViewScreenShot', 0),#sinonimo
    'documento de texto':    lambda: Gui.runCommand('Std_TextDocument', 0),
    'ayuda':       ayuda,
 }
##  Diccionario de referencia:
## explorer = {
##    'file':       file,
##    'edit':       edit,
##    'print':      print_cmds,
##    'doc':        doc,
##    'refresh':    lambda: Gui.runCommand('Std_Refresh', 0),
##    'screenshot': lambda: Gui.runCommand('Std_ViewScreenShot', 0),
##    'textdoc':    lambda: Gui.runCommand('Std_TextDocument', 0),
##    'help':       ayuda,
## }

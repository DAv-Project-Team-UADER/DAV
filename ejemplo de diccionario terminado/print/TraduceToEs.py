from doc import doc
from ayuda import ayuda
import FreeCADGui as Gui

TraduceToPtBr = {
    'imprimir': lambda: Gui.runCommand('Std_Print', 0),
    'normal': lambda: Gui.runCommand('Std_Print', 0),
    'papel': lambda: Gui.runCommand('Std_Print', 0),
    'pdf': lambda: Gui.runCommand('Std_PrintPdf', 0),
    'Ajuda': ayuda,
    'Assistência': ayuda,   # sinónimo adicional
}


# Como las claves originales ya son palabras idénticas o muy similares en portugués
# (imprimir, normal, papel), se mantienen igual. Si se desea una versión completamente
# en portugués, se podría cambiar 'papel' por 'papel' (igual) o 'folha', pero no es necesario.

#print_cmds = {
#    'print': lambda: Gui.runCommand('Std_Print', 0),
#    'pdf':   lambda: Gui.runCommand('Std_PrintPdf', 0),
#    'help':  ayuda,
#}

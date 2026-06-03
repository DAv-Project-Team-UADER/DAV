import FreeCADGui as Gui
from .ayuda import ayuda

def open_shapestring_tool():
    # Salir del croquis en modo edición de forma segura
    if Gui.ActiveDocument:
        try:
            if Gui.ActiveDocument.getInEdit():
                Gui.ActiveDocument.resetEdit()
        except AttributeError:
            pass 
        
    # Forzar el cierre de cualquier panel atascado (ignorando errores)
    try:
        Gui.Control.closeDialog()
    except Exception:
        pass
    
    # Activar Draft y disparar la herramienta
    Gui.activateWorkbench('DraftWorkbench')
    Gui.runCommand('Draft_ShapeString', 0)

text = {
    'create': open_shapestring_tool,
    'help':   ayuda
}
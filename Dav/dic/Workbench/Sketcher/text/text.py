# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)

import FreeCAD as App
import FreeCADGui as Gui
from .ayuda import ayuda
from selection.createobjects import CreateObjects

def open_shapestring_tool():
    if Gui.ActiveDocument:
        try:
            if Gui.ActiveDocument.getInEdit():
                Gui.ActiveDocument.resetEdit()
        except AttributeError:
            pass 
        
    try:
        Gui.Control.closeDialog()
    except Exception:
        pass
    
    Gui.activateWorkbench('DraftWorkbench')
    Gui.runCommand('Draft_ShapeString', 0)
    
    # Invocamos CreateObjects tras crear la forma de texto en Draft
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()

text = {
    'create': open_shapestring_tool,
    'help':   ayuda
}
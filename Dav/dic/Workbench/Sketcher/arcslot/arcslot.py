# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.

import FreeCAD as App
import FreeCADGui as Gui
from .ayuda import ayuda
from selection.createobjects import CreateObjects  # <-- Importamos tu clase del motor

def create_arc_slot_with_objects():
    """Ejecuta el comando de FreeCAD y extrae sus sub-elementos 2D."""
    # 1. Dispara el comando en la interfaz de FreeCAD
    Gui.runCommand('Sketcher_CreateArcSlot', 0)
    
    # 2. Verifica si hay un documento activo y un objeto recién creado
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        obj_name = active_doc.ActiveObject.Name
        
        # 3. Instancia la clase con el nombre del objeto (2D) y ejecuta el método
        creator = CreateObjects(ObjectName=obj_name, Is3D=False)
        creator.Execute()

arc_slot = {
    'arcends':  create_arc_slot_with_objects,
    'flatends': create_arc_slot_with_objects,
    'help':     ayuda,
}
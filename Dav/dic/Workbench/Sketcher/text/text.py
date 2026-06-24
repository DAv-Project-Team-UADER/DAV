# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#
# Este programa se distribuye con la esperanza de que sea útil,
# pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
# MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
# Licencia Pública General GNU para más detalles.
#
# Deberías haber recibido una copia de la Licencia Pública General GNU
# junto con este programa. Si no es así, consulte <http://www.gnu.org/licenses/>.
# SPDX-License-Identifier: GPL-3.0-or-later

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
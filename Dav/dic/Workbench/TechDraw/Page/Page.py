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

import FreeCADGui as Gui
from .ayuda import ayuda

# Diccionario del subgrupo Page (Gestión de lienzos de planos y salidas)
page = {
    'default': lambda: Gui.runCommand('TechDraw_PageDefault', 0),
    'template': lambda: Gui.runCommand('TechDraw_PageTemplate', 0),
    'redraw': lambda: Gui.runCommand('TechDraw_RedrawPage', 0),
    'print': lambda: Gui.runCommand('TechDraw_PrintAll', 0),
    'dxf': lambda: Gui.runCommand('TechDraw_ExportPageDXF', 0),
    'svg': lambda: Gui.runCommand('TechDraw_ExportPageSVG', 0),
    'help': ayuda
}
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

import FreeCADGui as Gui
from .ayuda import ayuda

views = {
    'view': lambda: Gui.runCommand('TechDraw_View', 0),
    'detailView': lambda: Gui.runCommand('TechDraw_DetailView', 0),
    'brokenView': lambda: Gui.runCommand('TechDraw_BrokenView', 0),
    'clipGroup': lambda: Gui.runCommand('TechDraw_ClipGroup', 0),
    'complexSection': lambda: Gui.runCommand('TechDraw_ComplexSection', 0),
    'draft': lambda: Gui.runCommand('TechDraw_DraftView', 0),
    'spreadsheet': lambda: Gui.runCommand('TechDraw_SpreadsheetView', 0),
    'help': ayuda
}
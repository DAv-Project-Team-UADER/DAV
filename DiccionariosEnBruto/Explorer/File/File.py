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

import FreeCAD
import FreeCADGui as Gui
from .ayuda import ayuda

file = {
    'new':      lambda: FreeCAD.newDocument(),
    'open':     lambda: Gui.runCommand('Std_Open', 0),
    'save':     lambda: FreeCAD.activeDocument().save(),
    'saveas':   lambda: Gui.runCommand('Std_SaveAs', 0),
    'savecopy': lambda: Gui.runCommand('Std_SaveCopy', 0),
    'revert':   lambda: Gui.runCommand('Std_Revert', 0),
    'merge':    lambda: Gui.runCommand('Std_MergeProjects', 0),
    'import':   lambda: Gui.runCommand('Std_Import', 0),
    'export':   lambda: Gui.runCommand('Std_Export', 0),
    'help':     ayuda,
}

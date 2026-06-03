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

link = {
    'make link': lambda: Gui.runCommand('Std_LinkMake', 0),
    'relative link': lambda: Gui.runCommand('Std_LinkMakeRelative', 0),
    'import link': lambda: Gui.runCommand('Std_LinkImport', 0),
    'import all links': lambda: Gui.runCommand('Std_LinkImportAll', 0),
    'replace link': lambda: Gui.runCommand('Std_LinkReplace', 0),
    'help': ayuda,
}
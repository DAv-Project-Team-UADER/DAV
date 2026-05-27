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

# Diccionario DAV - StdView / Tree
tree = {
    'collapse': lambda: Gui.runCommand('Std_TreeCollapseDocument', 0),
    'preselection': lambda: Gui.runCommand('Std_TreePreSelection', 0),
    'recordselection': lambda: Gui.runCommand('Std_TreeRecordSelection', 0),
    'singleexpand': lambda: Gui.runCommand('Std_TreeSingleExpand', 0),
    'syncplacement': lambda: Gui.runCommand('Std_TreeSyncPlacement', 0),
    'syncselection': lambda: Gui.runCommand('Std_TreeSyncSelection', 0),
    'syncview': lambda: Gui.runCommand('Std_TreeSyncView', 0),
}

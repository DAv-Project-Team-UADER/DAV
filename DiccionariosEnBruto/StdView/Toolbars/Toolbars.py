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

# Diccionario DAV - StdView / Toolbars
toolbars = {
    'clipboard': lambda: Gui.runCommand('Std_ToolbarClipboard', 0),
    'edit':      lambda: Gui.runCommand('Std_ToolbarEdit', 0),
    'file':      lambda: Gui.runCommand('Std_ToolbarFile', 0),
    'help':      lambda: Gui.runCommand('Std_ToolbarHelp', 0),
    'views':     lambda: Gui.runCommand('Std_ToolbarIndividualViews', 0),
    'lock':      lambda: Gui.runCommand('Std_ToggleToolbarsLock', 0),
    'macro':     lambda: Gui.runCommand('Std_ToolbarMacro', 0),
    'structure': lambda: Gui.runCommand('Std_ToolbarStructure', 0),
    'view':      lambda: Gui.runCommand('Std_ToolbarView', 0),
    'workbench': lambda: Gui.runCommand('Std_ToolbarWorkbench', 0),
}

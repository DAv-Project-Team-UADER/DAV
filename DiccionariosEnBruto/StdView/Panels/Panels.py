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

# Diccionario DAV - StdView / Panels
panels = {
    'panel': lambda: Gui.runCommand('Std_PanelView', 0),
    'dock': lambda: Gui.runCommand('Std_DockView', 0),
    'fullscreen': lambda: Gui.runCommand('Std_ViewFullscreen', 0),
    'undock': lambda: Gui.runCommand('Std_UndockView', 0),
    'dagview': lambda: Gui.runCommand('Std_DAGView', 0),
    'comboview': lambda: Gui.runCommand('Std_ComboView', 0),
    'selectionview': lambda: Gui.runCommand('Std_SelectionView', 0),
    'tasks': lambda: Gui.runCommand('Std_TaskView', 0),
    'properties': lambda: Gui.runCommand('Std_PropertyView', 0),
    'console': lambda: Gui.runCommand('Std_PythonConsole', 0),
    'report': lambda: Gui.runCommand('Std_ReportView', 0),
    'treeview': lambda: Gui.runCommand('Std_TreeView', 0),
    'statusbar': lambda: Gui.runCommand('Std_ViewStatusBar', 0),
}

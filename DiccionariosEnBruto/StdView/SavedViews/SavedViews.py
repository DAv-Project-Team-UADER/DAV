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

# Diccionario DAV - StdView / SavedViews
savedviews = {
    'clear':   lambda: Gui.runCommand('Std_ClearViews', 0),
    'freeze':  lambda: Gui.runCommand('Std_FreezeView', 0),
    'restore': lambda: Gui.runCommand('Std_FreezeViewsRestore', 0),
    'recall':  lambda: Gui.runCommand('Std_RecallWorkingView', 0),
    'load':    lambda: Gui.runCommand('Std_RestoreView', 0),
    'save':    lambda: Gui.runCommand('Std_FreezeViewsSave', 0),
    'store':   lambda: Gui.runCommand('Std_StoreWorkingView', 0),
}

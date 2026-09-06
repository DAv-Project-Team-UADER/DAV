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

def _restore_frozen_view():
    try:
        Gui.runCommand('Std_FreezeViews', 6)
    except Exception:
        try:
            Gui.runCommand('Std_ViewRestoreCamera', 0)
        except Exception:
            pass

# Diccionario DAV - StdView / SavedViews
savedviews = {
    'clear':   lambda: Gui.runCommand('Std_FreezeViews', 4),
    'freeze':  lambda: Gui.runCommand('Std_FreezeViews', 3),
    'restore': _restore_frozen_view,
    'recall':  lambda: Gui.runCommand('Std_RecallWorkingView', 0),
    'load':    lambda: Gui.runCommand('Std_FreezeViews', 1),
    'save':    lambda: Gui.runCommand('Std_FreezeViews', 0),
    'store':   lambda: Gui.runCommand('Std_StoreWorkingView', 0),
    'help':    ayuda,
}

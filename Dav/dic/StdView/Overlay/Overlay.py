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

def _toggle_floating():
    mw = Gui.getMainWindow() if hasattr(Gui, 'getMainWindow') else None
    if not mw:
        return
    focus = mw.focusWidget()
    while focus:
        if hasattr(focus, 'isFloating') and hasattr(focus, 'setFloating'):
            focus.setFloating(not focus.isFloating())
            return
        focus = focus.parentWidget()
    for child in mw.children():
        if hasattr(child, 'isFloating') and hasattr(child, 'setFloating') and child.isVisible():
            child.setFloating(not child.isFloating())
            return

# Diccionario DAV - StdView / Overlay
overlay = {
    'bottom':     lambda: Gui.runCommand('Std_DockOverlay', 11),
    'float':      _toggle_floating,
    'left':       lambda: Gui.runCommand('Std_DockOverlay', 8),
    'right':      lambda: Gui.runCommand('Std_DockOverlay', 9),
    'axis':       lambda: Gui.runCommand('Std_AxisCross', 0),
    'navigation': lambda: Gui.runCommand('Std_ToggleNavigation', 0),
    'toggle':     lambda: Gui.runCommand('Std_DockOverlay', 3),
    'help':       ayuda,
}

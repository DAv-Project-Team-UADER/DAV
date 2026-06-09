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

# Diccionario DAV - StdView / Visibility
visibility = {
    'hideobjects':      lambda: Gui.runCommand('Std_HideObjects', 0),
    'hide':             lambda: Gui.runCommand('Std_HideSelection', 0),
    'alllinks':         lambda: Gui.runCommand('Std_LinkSelectAllLinks', 0),
    'linked':           lambda: Gui.runCommand('Std_LinkSelectLinked', 0),
    'linkedfinal':      lambda: Gui.runCommand('Std_LinkSelectLinkedFinal', 0),
    'selback':          lambda: Gui.runCommand('Std_SelBack', 0),
    'boundingbox':      lambda: Gui.runCommand('Std_SelBoundingBox', 0),
    'selforward':       lambda: Gui.runCommand('Std_SelForward', 0),
    'selectvisible':    lambda: Gui.runCommand('Std_SelectVisibleObjects', 0),
    'showobjects':      lambda: Gui.runCommand('Std_ShowObjects', 0),
    'show':             lambda: Gui.runCommand('Std_ShowSelection', 0),
    'toggleall':        lambda: Gui.runCommand('Std_ToggleObjects', 0),
    'selectability':    lambda: Gui.runCommand('Std_ToggleSelectability', 0),
    'transparency':     lambda: Gui.runCommand('Std_ToggleTransparency', 0),
    'toggle':           lambda: Gui.runCommand('Std_ToggleVisibility', 0),
    'aligntoselection': lambda: Gui.runCommand('Std_AlignToSelection', 0),
    'help':             ayuda,
}

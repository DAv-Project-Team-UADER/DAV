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

geometric = {
    'coincident':          lambda: Gui.runCommand('Sketcher_ConstrainCoincident', 0),
    'coincidentunified':   lambda: Gui.runCommand('Sketcher_ConstrainCoincidentUnified', 0),
    'lock':                lambda: Gui.runCommand('Sketcher_ConstrainLock', 0),
    'pointonobject':       lambda: Gui.runCommand('Sketcher_ConstrainPointOnObject', 0),
    'horizontal':          lambda: Gui.runCommand('Sketcher_ConstrainHorizontal', 0),
    'vertical':            lambda: Gui.runCommand('Sketcher_ConstrainVertical', 0),
    'horver':              lambda: Gui.runCommand('Sketcher_ConstrainHorVer', 0),
    'parallel':            lambda: Gui.runCommand('Sketcher_ConstrainParallel', 0),
    'perpendicular':       lambda: Gui.runCommand('Sketcher_ConstrainPerpendicular', 0),
    'tangent':             lambda: Gui.runCommand('Sketcher_ConstrainTangent', 0),
    'equal':               lambda: Gui.runCommand('Sketcher_ConstrainEqual', 0),
    'symmetric':           lambda: Gui.runCommand('Sketcher_ConstrainSymmetric', 0),
    'block':               lambda: Gui.runCommand('Sketcher_ConstrainBlock', 0),
    'toggledriving':       lambda: Gui.runCommand('Sketcher_ToggleDrivingReference', 0),
    'toggleactive':        lambda: Gui.runCommand('Sketcher_ToggleConstraints', 0),
    'help':                ayuda,
}

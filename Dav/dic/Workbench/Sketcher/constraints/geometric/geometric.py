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
from .. import _voice

geometric = {
    'coincident':          _voice.make_coincident,
    'coincidentunified':   lambda: Gui.runCommand('Sketcher_ConstrainCoincidentUnified', 0),
    'lock':                lambda: Gui.runCommand('Sketcher_ConstrainLock', 0),
    'pointonobject':       _voice.make_point_on_object,
    'horizontal':          _voice.make_horizontal,
    'vertical':            _voice.make_vertical,
    'horver':              lambda: Gui.runCommand('Sketcher_ConstrainHorVer', 0),
    'parallel':            _voice.make_parallel,
    'perpendicular':       _voice.make_perpendicular,
    'tangent':             _voice.make_tangent,
    'equal':               _voice.make_equal,
    'symmetric':           _voice.make_symmetric,
    'block':               _voice.make_block,
    'toggledriving':       lambda: Gui.runCommand('Sketcher_ToggleDrivingReference', 0),
    'toggleactive':        lambda: Gui.runCommand('Sketcher_ToggleConstraints', 0),
    'help':                ayuda,
}

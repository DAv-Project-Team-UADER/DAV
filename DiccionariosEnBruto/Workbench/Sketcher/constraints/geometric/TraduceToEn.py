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
# SPDX-License-Identifier: GPL-3.0-or-later

"""English spoken-word mapping for the geometric dictionary."""

import FreeCADGui as Gui
from .ayuda import ayuda

TraduceToEn = {
    # Coincidencia
    'coincident':           lambda: Gui.runCommand('Sketcher_ConstrainCoincident', 0),
    'make coincident':      lambda: Gui.runCommand('Sketcher_ConstrainCoincident', 0),
    'join points':          lambda: Gui.runCommand('Sketcher_ConstrainCoincident', 0),

    # Coincidencia unificada
    'coincident unified':   lambda: Gui.runCommand('Sketcher_ConstrainCoincidentUnified', 0),
    'unified coincident':   lambda: Gui.runCommand('Sketcher_ConstrainCoincidentUnified', 0),

    # Bloqueo de posición (lock)
    'lock':                 lambda: Gui.runCommand('Sketcher_ConstrainLock', 0),
    'fix position':         lambda: Gui.runCommand('Sketcher_ConstrainLock', 0),

    # Punto sobre objeto
    'point on object':      lambda: Gui.runCommand('Sketcher_ConstrainPointOnObject', 0),
    'fix to line':          lambda: Gui.runCommand('Sketcher_ConstrainPointOnObject', 0),

    # Horizontal y Vertical
    'horizontal':           lambda: Gui.runCommand('Sketcher_ConstrainHorizontal', 0),
    'make horizontal':      lambda: Gui.runCommand('Sketcher_ConstrainHorizontal', 0),
    
    'vertical':             lambda: Gui.runCommand('Sketcher_ConstrainVertical', 0),
    'make vertical':        lambda: Gui.runCommand('Sketcher_ConstrainVertical', 0),
    
    'horizontal vertical':  lambda: Gui.runCommand('Sketcher_ConstrainHorVer', 0),
    'auto orientation':     lambda: Gui.runCommand('Sketcher_ConstrainHorVer', 0),

    # Paralelismo y Perpendicularidad
    'parallel':             lambda: Gui.runCommand('Sketcher_ConstrainParallel', 0),
    'make parallel':        lambda: Gui.runCommand('Sketcher_ConstrainParallel', 0),
    
    'perpendicular':        lambda: Gui.runCommand('Sketcher_ConstrainPerpendicular', 0),
    'make perpendicular':   lambda: Gui.runCommand('Sketcher_ConstrainPerpendicular', 0),

    # Tangencia
    'tangent':              lambda: Gui.runCommand('Sketcher_ConstrainTangent', 0),
    'make tangent':         lambda: Gui.runCommand('Sketcher_ConstrainTangent', 0),

    # Igualdad
    'equal':                lambda: Gui.runCommand('Sketcher_ConstrainEqual', 0),
    'make equal':           lambda: Gui.runCommand('Sketcher_ConstrainEqual', 0),
    'equal length':         lambda: Gui.runCommand('Sketcher_ConstrainEqual', 0),

    # Simetría
    'symmetric':            lambda: Gui.runCommand('Sketcher_ConstrainSymmetric', 0),
    'make symmetric':       lambda: Gui.runCommand('Sketcher_ConstrainSymmetric', 0),
    'symmetry':             lambda: Gui.runCommand('Sketcher_ConstrainSymmetric', 0),

    # Bloqueo general (block)
    'block':                lambda: Gui.runCommand('Sketcher_ConstrainBlock', 0),
    'block geometry':       lambda: Gui.runCommand('Sketcher_ConstrainBlock', 0),

    # Alternar conductora/referencia (toggledriving)
    'toggle driving':       lambda: Gui.runCommand('Sketcher_ToggleDrivingReference', 0),
    'reference mode':       lambda: Gui.runCommand('Sketcher_ToggleDrivingReference', 0),
    'driving mode':         lambda: Gui.runCommand('Sketcher_ToggleDrivingReference', 0),

    # Activar/desactivar restricción (toggleactive)
    'toggle active':        lambda: Gui.runCommand('Sketcher_ToggleConstraints', 0),
    'activate constraint':  lambda: Gui.runCommand('Sketcher_ToggleConstraints', 0),
    'deactivate constraint':lambda: Gui.runCommand('Sketcher_ToggleConstraints', 0),

    # Comandos de ayuda
    'help':                 ayuda,
    'commands':             ayuda,
    'options':              ayuda
}

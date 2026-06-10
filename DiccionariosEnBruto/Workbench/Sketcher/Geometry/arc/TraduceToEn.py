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

"""English spoken-word mapping for the arc dictionary."""

import FreeCADGui as Gui
from .ayuda import ayuda

TraduceToEn = {
    # Comandos para crear arco desde el centro
    'center':           lambda: Gui.runCommand('Sketcher_CreateArc', 0),
    'arc by center':    lambda: Gui.runCommand('Sketcher_CreateArc', 0),
    'center arc':       lambda: Gui.runCommand('Sketcher_CreateArc', 0),

    # Comandos para crear arco mediante 3 puntos
    'three point':      lambda: Gui.runCommand('Sketcher_Create3PointArc', 0),
    'three points':     lambda: Gui.runCommand('Sketcher_Create3PointArc', 0),
    '3 point':          lambda: Gui.runCommand('Sketcher_Create3PointArc', 0),
    '3 points':         lambda: Gui.runCommand('Sketcher_Create3PointArc', 0),
    'arc by 3 points':  lambda: Gui.runCommand('Sketcher_Create3PointArc', 0),

    # Comandos de ayuda integrados
    'help':             ayuda,
    'commands':         ayuda,
    'options':          ayuda
}

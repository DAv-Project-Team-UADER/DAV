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

"""English spoken-word mapping for the arc_slot dictionary."""

import FreeCADGui as Gui
from .ayuda import ayuda

TraduceToEn = {
    # Comandos para crear ranura curva con bordes redondeados (arc_ends)
    'arc ends':         lambda: Gui.runCommand('Sketcher_CreateArcSlot', 0),
    'rounded slot':     lambda: Gui.runCommand('Sketcher_CreateArcSlot', 0),
    'curved slot':      lambda: Gui.runCommand('Sketcher_CreateArcSlot', 0),
    'arc slot':         lambda: Gui.runCommand('Sketcher_CreateArcSlot', 0),

    # Comandos para crear ranura curva con bordes planos (flat_ends)
    'flat ends':        lambda: Gui.runCommand('Sketcher_CreateArcSlot', 0),
    'flat slot':        lambda: Gui.runCommand('Sketcher_CreateArcSlot', 0),
    'square ends':      lambda: Gui.runCommand('Sketcher_CreateArcSlot', 0),
    'flat arc slot':    lambda: Gui.runCommand('Sketcher_CreateArcSlot', 0),

    # Comandos de ayuda integrados
    'help':             ayuda,
    'commands':         ayuda,
    'options':          ayuda
}

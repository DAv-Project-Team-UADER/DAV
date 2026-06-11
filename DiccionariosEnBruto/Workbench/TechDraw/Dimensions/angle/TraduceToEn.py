# Copyright (C) 2026 El Equipo del Proyecto DAV
# Copyright (C) 2026 The DAV Project Team
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

import FreeCAD as App
import FreeCADGui as Gui
from .ayuda import ayuda
from .angle import _create_angle, _create_angle_3pt

TraduceToEn = {
    'angle':              lambda: _create_angle(),
    'angular':            lambda: _create_angle(),        # synonym
    'angle dimension':    lambda: _create_angle(),        # synonym
    'points':             lambda: _create_angle_3pt(),
    'three points':       lambda: _create_angle_3pt(),    # synonym
    'angle three points': lambda: _create_angle_3pt(),    # synonym
    '3 point angle':      lambda: _create_angle_3pt(),    # synonym
    'help':               ayuda,
    'assistance':         ayuda,  # synonym
}

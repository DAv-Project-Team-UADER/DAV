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

"""English spoken-word mapping for the constraints dictionary."""

from .constraints import constraints

TraduceToEn = {
    # Apunta a los elementos del diccionario original 'constraints'
    'dimension':            constraints['dimension'],
    'add dimension':        constraints['dimension'],
    'length':               constraints['dimension'],

    'horizontal':           constraints['horizontal'],
    'horizontal dimension': constraints['horizontal'],
    'horizontal distance':  constraints['horizontal'],

    'vertical':             constraints['vertical'],
    'vertical dimension':   constraints['vertical'],
    'vertical distance':    constraints['vertical'],

    'angle':                constraints['angle'],
    'angle dimension':      constraints['angle'],

    'radius':               constraints['radius'],
    'radius dimension':     constraints['radius'],

    'diameter':             constraints['diameter'],
    'diameter dimension':   constraints['diameter'],

    'radiam':               constraints['radiam'],
    'auto dimension':       constraints['radiam'],

    'distance':             constraints['distance'],
    'distance dimension':   constraints['distance'],

    'geometric':            constraints['geometric'],
    'geometric constraints':constraints['geometric'],
    'geometry constraints': constraints['geometric'],

    # Sinónimos para la función ayuda
    'help':                 constraints['help'],
    'commands':             constraints['help'],
    'options':              constraints['help']
}

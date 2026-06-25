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

"""Spanish spoken-word mapping for the constraints dictionary."""

from .constraints import constraints

TraduceToEs = {
    'dimension':            constraints['dimension'],
    'cota':                 constraints['dimension'],
    'longitud':             constraints['dimension'],

    'horizontal':           constraints['horizontal'],
    'cota horizontal':      constraints['horizontal'],
    'distancia horizontal': constraints['horizontal'],

    'vertical':             constraints['vertical'],
    'cota vertical':        constraints['vertical'],
    'distancia vertical':   constraints['vertical'],

    'angulo':               constraints['angle'],
    'cota angular':         constraints['angle'],

    'radio':                constraints['radius'],
    'cota radial':          constraints['radius'],

    'diametro':             constraints['diameter'],
    'cota diametral':       constraints['diameter'],

    'radiam':               constraints['radiam'],
    'cota automatica':      constraints['radiam'],

    'distancia':            constraints['distance'],
    'cota de distancia':    constraints['distance'],

    'geometrica':           constraints['geometric'],
    'restricciones':        constraints['geometric'],

    'ayuda':                constraints['help'],
    'información':             constraints['help'],
    'opciones':             constraints['help']
}

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

"""Portuguese spoken-word mapping for the constraints dictionary."""

from .constraints import constraints

TraduceToPt = {
    'dimensão':             constraints['dimension'],
    'cota':                 constraints['dimension'],
    'comprimento':          constraints['dimension'],

    'horizontal':           constraints['horizontal'],
    'cota horizontal':      constraints['horizontal'],
    'distância horizontal': constraints['horizontal'],

    'vertical':             constraints['vertical'],
    'cota vertical':        constraints['vertical'],
    'distância vertical':   constraints['vertical'],

    'ângulo':               constraints['angle'],
    'cota angular':         constraints['angle'],

    'raio':                 constraints['radius'],
    'cota radial':          constraints['radius'],

    'diâmetro':             constraints['diameter'],
    'cota diametral':       constraints['diameter'],

    'radiam':               constraints['radiam'],
    'cota automática':      constraints['radiam'],

    'distância':            constraints['distance'],
    'cota de distância':    constraints['distance'],

    'geométrica':           constraints['geometric'],
    'restrições':           constraints['geometric'],

    'ajuda':                constraints['help'],
    'informação':             constraints['help'],
    'opções':               constraints['help']
}

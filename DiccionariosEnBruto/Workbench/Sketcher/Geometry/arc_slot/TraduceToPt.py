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
"""Portuguese spoken-word mapping for the arc_slot dictionary."""

from .arc_slot import arc_slot

TraduceToPt = {
    'bordas arredondadas':  arc_slot['arc_ends'],
    'ranhura arredondada':  arc_slot['arc_ends'],
    'extremidades curvas':  arc_slot['arc_ends'],
    'ranhura curva':        arc_slot['arc_ends'],

    'bordas planas':        arc_slot['flat_ends'],
    'ranhura plana':        arc_slot['flat_ends'],
    'extremidades planas':  arc_slot['flat_ends'],
    'ranhura reta':         arc_slot['flat_ends'],

    'ajuda':                arc_slot['help'],
    'informação':             arc_slot['help'],
    'opções':               arc_slot['help']
}

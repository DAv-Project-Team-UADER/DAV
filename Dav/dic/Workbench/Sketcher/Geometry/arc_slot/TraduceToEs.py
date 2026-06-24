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

"""Spanish spoken-word mapping for the arc_slot dictionary."""

from .arc_slot import arc_slot

TraduceToEs = {
    'bordes redondeados':   arc_slot['arc_ends'],
    'ranura redondeada':    arc_slot['arc_ends'],
    'extremos curvos':      arc_slot['arc_ends'],
    'ranura curva':         arc_slot['arc_ends'],

    'bordes planos':        arc_slot['flat_ends'],
    'ranura plana':         arc_slot['flat_ends'],
    'extremos planos':      arc_slot['flat_ends'],
    'ranura recta':         arc_slot['flat_ends'],

    'ayuda':                arc_slot['help'],
    'comandos':             arc_slot['help'],
    'opciones':             arc_slot['help']
}

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

from .arc_slot import arc_slot

TraduceToEn = {
    # Apunta a los elementos del diccionario original 'arc_slot'
    'arc ends':         arc_slot['arc_ends'],
    'rounded slot':     arc_slot['arc_ends'],
    'curved slot':      arc_slot['arc_ends'],
    'arc slot':         arc_slot['arc_ends'],

    'flat ends':        arc_slot['flat_ends'],
    'flat slot':        arc_slot['flat_ends'],
    'square ends':      arc_slot['flat_ends'],
    'flat arc slot':    arc_slot['flat_ends'],

    # Sinónimos para la función ayuda
    'help':             arc_slot['help'],
    'info':         arc_slot['help'],
    'options':          arc_slot['help']
}

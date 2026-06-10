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

from .workbench import draft
from .ayuda import ayuda

TraduceToEn = {
    'annotation': draft['annotation'],
    'note':       draft['annotation'],
    'text':       draft['annotation'],

    'arc':        draft['arc'],

    'curve':      draft['curve'],
    'spline':     draft['curve'],
    'b-spline':   draft['curve'],

    'circle':     draft['circle'],

    'array':      draft['array'],
    'pattern':    draft['array'],
    'circular array': draft['array'],

    'modify':     draft['modify'],
    'edit':       draft['modify'],
    'change':     draft['modify'],

    'dimension':  draft['dimension'],
    'measure':    draft['dimension'],
    'measurement': draft['dimension'],

    'ellipse':    draft['ellipse'],
    'oval':       draft['ellipse'],

    'facebinder': draft['facebinder'],
    'binder':     draft['facebinder'],
    'face binder': draft['facebinder'],

    'help':       ayuda,
    'support':    ayuda,
}

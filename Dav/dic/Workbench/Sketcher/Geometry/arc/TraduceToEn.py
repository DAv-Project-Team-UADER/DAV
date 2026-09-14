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

from .arc import arc

TraduceToEn = {
    # Apunta a los elementos del diccionario original 'arc'
    'center':           arc['center'],
    'arc by center':    arc['center'],
    'center arc':       arc['center'],

    'three point':      arc['3point'],
    'three points':     arc['3point'],
    '3 point':          arc['3point'],
    '3 points':         arc['3point'],
    'arc by 3 points':  arc['3point'],

    # Sinónimos para la función ayuda
    'help':             arc['help'],
    'info':         arc['help'],
    'options':          arc['help'],

    # Arc by dictated coordinates
    "arc by center": arc['create_by_center'],
    "create arc by center": arc['create_by_center'],
    "arc by angles": arc['create_by_center'],
    "arc by coordinates": arc['create_by_center'],
}

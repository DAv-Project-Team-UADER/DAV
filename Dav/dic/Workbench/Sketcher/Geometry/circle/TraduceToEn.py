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

"""English spoken-word mapping for the circle dictionary."""

from .circle import circle

TraduceToEn = {
    # Apunta a los elementos del diccionario original 'circle'
    'create':           circle['create'],
    'circle':           circle['create'],
    'center circle':    circle['create'],
    'circle by center': circle['create'],

    'three point':      circle['3point'],
    'three points':     circle['3point'],
    '3 point':          circle['3point'],
    '3 points':         circle['3point'],
    'circle by 3 points': circle['3point'],

    # Sinónimos para la función ayuda
    'help':             circle['help'],
    'info':         circle['help'],
    'options':          circle['help'],

    # Circle by dictated coordinates
    "circle by center": circle['create_by_center'],
    "create circle by center": circle['create_by_center'],
    "circle by radius": circle['create_by_center'],
    "circle by coordinates": circle['create_by_center'],
}

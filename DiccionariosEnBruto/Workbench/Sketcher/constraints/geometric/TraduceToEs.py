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

"""Spanish spoken-word mapping for the geometric dictionary."""

from .geometric import geometric

TraduceToEs = {
    'coincidente':          geometric['coincident'],
    'hacer coincidente':    geometric['coincident'],
    'unir puntos':          geometric['coincident'],

    'coincidente unificado': geometric['coincidentunified'],
    'coincidencia unificada':geometric['coincidentunified'],

    'bloquear':             geometric['lock'],
    'fijar posicion':       geometric['lock'],

    'punto en objeto':      geometric['pointonobject'],
    'fijar a linea':        geometric['pointonobject'],

    'horizontal':           geometric['horizontal'],
    'hacer horizontal':     geometric['horizontal'],
    
    'vertical':             geometric['vertical'],
    'hacer vertical':       geometric['vertical'],
    
    'horizontal vertical':  geometric['horver'],
    'orientacion automatica':geometric['horver'],

    'paralelo':             geometric['parallel'],
    'hacer paralelo':       geometric['parallel'],
    
    'perpendicular':        geometric['perpendicular'],
    'hacer perpendicular':  geometric['perpendicular'],

    'tangente':             geometric['tangent'],
    'hacer tangente':       geometric['tangent'],

    'igual':                geometric['equal'],
    'hacer igual':          geometric['equal'],
    'longitud igual':       geometric['equal'],

    'simetrico':            geometric['symmetric'],
    'hacer simetrico':      geometric['symmetric'],
    'simetria':             geometric['symmetric'],

    'bloque':               geometric['block'],
    'bloquear geometria':   geometric['block'],

    'alternar conductora':  geometric['toggledriving'],
    'modo referencia':      geometric['toggledriving'],

    'alternar activa':      geometric['toggleactive'],
    'activar restriccion':  geometric['toggleactive'],
    'desactivar restriccion':geometric['toggleactive'],

    'ayuda':                geometric['help'],
    'información':             geometric['help'],
    'opciones':             geometric['help']
}

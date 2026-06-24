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

"""Portuguese spoken-word mapping for the geometric dictionary."""

from .geometric import geometric

TraduceToPt = {
    'coincidente':          geometric['coincident'],
    'fazer coincidente':    geometric['coincident'],
    'unir pontos':          geometric['coincident'],

    'coincidente unificado': geometric['coincidentunified'],
    'coincidência unificada':geometric['coincidentunified'],

    'bloquear':             geometric['lock'],
    'fixar posição':        geometric['lock'],

    'ponto no objeto':      geometric['pointonobject'],
    'fixar na linha':       geometric['pointonobject'],

    'horizontal':           geometric['horizontal'],
    'fazer horizontal':     geometric['horizontal'],
    
    'vertical':             geometric['vertical'],
    'fazer vertical':       geometric['vertical'],
    
    'horizontal vertical':  geometric['horver'],
    'orientação automática': geometric['horver'],

    'paralelo':             geometric['parallel'],
    'fazer paralelo':       geometric['parallel'],
    
    'perpendicular':        geometric['perpendicular'],
    'fazer perpendicular':  geometric['perpendicular'],

    'tangente':             geometric['tangent'],
    'fazer tangente':       geometric['tangent'],

    'igual':                geometric['equal'],
    'fazer igual':          geometric['equal'],
    'comprimento igual':    geometric['equal'],

    'simétrico':            geometric['symmetric'],
    'fazer simétrico':      geometric['symmetric'],
    'simetria':             geometric['symmetric'],

    'bloco':                geometric['block'],
    'bloquear geometria':   geometric['block'],

    'alternar condutora':   geometric['toggledriving'],
    'modo referência':      geometric['toggledriving'],

    'alternar ativa':       geometric['toggleactive'],
    'ativar restrição':     geometric['toggleactive'],
    'desativar restrição':  geometric['toggleactive'],

    'ajuda':                geometric['help'],
    'comandos':             geometric['help'],
    'opções':               geometric['help']
}

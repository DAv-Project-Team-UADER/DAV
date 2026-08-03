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

"""Spanish spoken-word mapping for the overlay dictionary."""

from .Overlay import overlay

TraduceToEs = {
    # Posiciones y visualización de superposición (overlay)
    'abajo':                    overlay['bottom'],
    'panel inferior':           overlay['bottom'],
    'superposición abajo':      overlay['bottom'],

    'flotar':                   overlay['float'],
    'panel flotante':           overlay['float'],
    'superposición flotante':   overlay['float'],

    'izquierda':                overlay['left'],
    'panel izquierdo':          overlay['left'],
    'superposición izquierda':  overlay['left'],

    'derecha':                  overlay['right'],
    'panel derecho':            overlay['right'],
    'superposición derecha':    overlay['right'],

    'eje':                      overlay['axis'],
    'cruz de ejes':             overlay['axis'],
    'mostrar ejes':             overlay['axis'],

    'navegación':               overlay['navigation'],
    'alternar navegación':      overlay['navigation'],
    'panel de navegación':      overlay['navigation'],

    'alternar':                 overlay['toggle'],
    'alternar superposición':   overlay['toggle'],
    'mostrar panel':            overlay['toggle'],

    # Comandos de ayuda estandarizados
    'ayuda':                    overlay['help'],
    'información':              overlay['help'],
    'opciones':                 overlay['help']
}

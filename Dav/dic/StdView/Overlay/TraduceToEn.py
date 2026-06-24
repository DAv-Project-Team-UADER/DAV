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

"""English spoken-word mapping for the overlay dictionary."""

from .overlay import overlay

TraduceToEn = {
    # Overlay positions and toggles
    'bottom':           overlay['bottom'],
    'bottom overlay':   overlay['bottom'],
    'overlay bottom':   overlay['bottom'],

    'float':            overlay['float'],
    'floating overlay': overlay['float'],
    'float overlay':    overlay['float'],

    'left':             overlay['left'],
    'left overlay':     overlay['left'],
    'overlay left':     overlay['left'],

    'right':            overlay['right'],
    'right overlay':    overlay['right'],
    'overlay right':    overlay['right'],

    'axis':             overlay['axis'],
    'axis cross':       overlay['axis'],
    'show axis':        overlay['axis'],

    'navigation':       overlay['navigation'],
    'toggle navigation':overlay['navigation'],
    'navigation panel': overlay['navigation'],

    'toggle':           overlay['toggle'],
    'toggle overlay':   overlay['toggle'],
    'show overlay':     overlay['toggle'],

    # Comandos de ayuda estandarizados
    'help':             overlay['help'],
    'commands':         overlay['help'],
    'options':          overlay['help']
}

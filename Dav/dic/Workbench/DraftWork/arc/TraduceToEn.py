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

"""English spoken-word mapping for the Arc dictionary."""

from .arc import arc

TraduceToEn = {
    # Draft Arc
    "center":             arc['center'],
    "center arc":         arc['center'],
    "arc by center":      arc['center'],
    "standard arc":       arc['center'],
    "radius arc":         arc['center'],

    # Draft Arc 3Points
    "points":             arc['points'],
    "3 points":           arc['points'],
    "three points":       arc['points'],
    "arc by 3 points":    arc['points'],
    "arc by three points":arc['points'],
    "3 point arc":        arc['points'],

    "help":               arc['help'],
    "info":               arc['help'],
    "options":            arc['help']
}
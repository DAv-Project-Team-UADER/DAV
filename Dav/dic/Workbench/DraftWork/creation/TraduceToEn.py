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

"""English spoken-word mapping for the Creation dictionary."""

from .creation import creation

TraduceToEn = {
    # Draft Hatch
    "hatch":           creation['hatch'],
    "fill pattern":    creation['hatch'],
    "hatch pattern":   creation['hatch'],
    "pattern":         creation['hatch'],

    # Draft Point
    "point":           creation['point'],
    "create point":    creation['point'],
    "dot":             creation['point'],

    # Draft Polygon
    "polygon":         creation['polygon'],
    "regular polygon": creation['polygon'],
    "create polygon":  creation['polygon'],

    # Draft Rectangle
    "rectangle":       creation['rectangle'],
    "create rectangle":creation['rectangle'],
    "box":             creation['rectangle'],

    "help":            creation['help'],
    "info":            creation['help'],
    "options":         creation['help']
}
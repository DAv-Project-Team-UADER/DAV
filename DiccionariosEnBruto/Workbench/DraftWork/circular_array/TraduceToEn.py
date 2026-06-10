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

"""English spoken-word mapping for the Array dictionary."""

from .array import array

TraduceToEn = {
    # Circular Array
    "circular":           array['circular'],
    "circular array":     array['circular'],
    "concentric array":   array['circular'],

    # Ortho Array
    "ortho":              array['ortho'],
    "ortho array":        array['ortho'],
    "orthogonal":         array['ortho'],
    "orthogonal array":   array['ortho'],
    "rectangular array":  array['ortho'],

    # Polar Array
    "polar":              array['polar'],
    "polar array":        array['polar'],

    # Path Array
    "path":               array['path'],
    "path array":         array['path'],
    "along path":         array['path'],
    "array along curve":  array['path'],

    # Path Link Array
    "path link":          array['pathlink'],
    "path link array":    array['pathlink'],
    "link path array":    array['pathlink'],
    "link along path":    array['pathlink'],

    # Point Array
    "point":              array['point'],
    "point array":        array['point'],
    "array by points":    array['point'],

    # Point Link Array
    "point link":         array['pointlink'],
    "point link array":   array['pointlink'],
    "link point array":   array['pointlink'],
    "link by points":     array['pointlink'],

    "help":               array['help'],
    "info":               array['help'],
    "options":            array['help']
}
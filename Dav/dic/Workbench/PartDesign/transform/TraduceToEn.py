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

"""English spoken-word mapping for PartDesign transform commands."""

from .transform import transform
from .ayuda import ayuda

TraduceToEn = {
    # Linear Pattern
    "linear pattern": transform["linearpattern"],
    "linear": transform["linearpattern"],

    # Mirrored
    "mirrored": transform["mirrored"],
    "mirror": transform["mirrored"],

    # Polar Pattern
    "polar pattern": transform["polarpattern"],
    "polar": transform["polarpattern"],
    "circular pattern": transform["polarpattern"],

    # Multi Transform
    "multi transform": transform["multitransform"],
    "multi": transform["multitransform"],

    # Scaled
    "scaled": transform["scaled"],
    "scale": transform["scaled"],
    "resize": transform["scaled"],

    # Help
    "help": transform['help'],
    # Patterns by dictated measure (no dialog)
    "linear pattern by length":   transform["linear_pattern"],
    "repeat in line":             transform["linear_pattern"],

    "linear pattern by spacing":  transform["linear_pattern_by_spacing"],
    "repeat every":               transform["linear_pattern_by_spacing"],

    "polar pattern by angle":     transform["polar_pattern"],
    "repeat in circle":           transform["polar_pattern"],

    "scale by factor":            transform["scaled_by_factor"],
    "scale solid":                transform["scaled_by_factor"],

    "info": transform['help'],
    "options": transform['help'],
}


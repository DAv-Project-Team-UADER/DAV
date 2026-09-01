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

"""Mapeo de comandos hablados en español para PartDesign transform."""

from .transform import transform
from .ayuda import ayuda

TraduceToEs = {
    # Patrón lineal
    "patron lineal": transform["linearpattern"],
    "lineal": transform["linearpattern"],

    # Espejo
    "simetria": transform["mirrored"],
    "espejo": transform["mirrored"],

    # Patrón polar
    "patron polar": transform["polarpattern"],
    "polar": transform["polarpattern"],
    "patron circular": transform["polarpattern"],

    # Multitransformación
    "multitransformacion": transform["multitransform"],
    "multi": transform["multitransform"],

    # Escalado
    "escalado": transform["scaled"],
    "escalar": transform["scaled"],
    "redimensionar": transform["scaled"],

    # Ayuda
    # Patrones por medida dictada (sin dialogo)
    "patron lineal por medida":   transform["linear_pattern"],
    "repetir en linea":           transform["linear_pattern"],
    "patron lineal":              transform["linear_pattern"],

    "patron lineal por separacion": transform["linear_pattern_by_spacing"],
    "repetir cada":               transform["linear_pattern_by_spacing"],

    "patron circular por medida": transform["polar_pattern"],
    "patron polar por medida":    transform["polar_pattern"],
    "repetir en circulo":         transform["polar_pattern"],

    "escalar por factor":         transform["scaled_by_factor"],
    "escalar solido":             transform["scaled_by_factor"],

    "ayuda": transform['help'],
    "información": transform['help'],
    "opciones": transform['help'],
}

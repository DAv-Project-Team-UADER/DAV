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

"""Mapeamento de comandos falados em português para PartDesign transform."""

from .transform import transform
from .ayuda import ayuda

TraduceToPt = {
    # Padrão linear
    "padrao linear": transform["linearpattern"],
    "linear": transform["linearpattern"],

    # Espelho
    "espelhado": transform["mirrored"],
    "espelho": transform["mirrored"],

    # Padrão polar
    "padrao polar": transform["polarpattern"],
    "polar": transform["polarpattern"],
    "padrao circular": transform["polarpattern"],

    # Multitransformação
    "multitransformacao": transform["multitransform"],
    "multi": transform["multitransform"],

    # Escala
    "escalado": transform["scaled"],
    "escalar": transform["scaled"],
    "redimensionar": transform["scaled"],

    # Ajuda
    "ajuda": transform['help'],
    "informação": transform['help'],
    "opções": transform['help'],
}

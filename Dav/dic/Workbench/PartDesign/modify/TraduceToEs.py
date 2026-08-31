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

from .modify import modify
from .ayuda import ayuda

TraduceToEs = {
    # Fillet
    "redondeo": modify["fillet"],
    "redondear": modify["fillet"],

    # Chamfer
    "chaflan": modify["chamfer"],
    "bisel": modify["chamfer"],
    "chaflanar": modify["chamfer"],
    "biselar": modify["chamfer"],

    # Draft
    "inclinacion": modify["draft"],
    "desmoldeo": modify["draft"],
    "inclinacion de cara": modify["draft"],
    "desmoldeo de cara": modify["draft"],

    # Thickness
    "espesor": modify["thickness"],
    "grosor": modify["thickness"],
    "agregar espesor": modify["thickness"],
    "agregar grosor": modify["thickness"],

    # Acabados por medida dictada (sin dialogo)
    "redondear por radio":   modify["fillet_by_radius"],
    "redondeo por radio":    modify["fillet_by_radius"],
    "redondear aristas":     modify["fillet_by_radius"],

    "chaflan por medida":    modify["chamfer_by_size"],
    "achaflanar por medida": modify["chamfer_by_size"],
    "chaflan por tamano":    modify["chamfer_by_size"],

    "chaflan por medida y angulo": modify["chamfer_by_size_and_angle"],
    "chaflan con angulo":    modify["chamfer_by_size_and_angle"],

    "espesor por medida":    modify["thickness_by_value"],
    "vaciar solido":         modify["thickness_by_value"],

    # Help
    "ayuda":                modify["help"],
    "información":          modify["help"],
    "opciones":             modify["help"]
}

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

TraduceToEs = {
    "clonar": modify["clone"],
    "copiar": modify["clone"],

    "simplificar": modify["downgrade"],
    "degradar": modify["downgrade"],

    "boceto": modify["sketch"],
    "convertir a boceto": modify["sketch"],

    "editar": modify["edit"],
    "modificar": modify["edit"],

    "redondear": modify["fillet"],
    "filete": modify["fillet"],

    "unir": modify["join"],
    "combinar": modify["join"],

    "mover": modify["move"],
    "desplazar": modify["move"],

    "desfase": modify["offset"],
    "offset": modify["offset"],

    "rotar": modify["rotate"],
    "girar": modify["rotate"],

    "espejo": modify["mirror"],
    "reflejar": modify["mirror"],

    "ayuda":                modify["help"],
    "información":          modify["help"],
    "opciones":            modify["help"]


}
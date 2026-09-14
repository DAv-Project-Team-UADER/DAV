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

"""Spanish spoken-word mapping for Part make face commands."""

from .part_makeface import part_makeface

from .ayuda import ayuda

TraduceToEs = {
    "cara": part_makeface["makeface"],
    "crear cara": part_makeface["makeface"],
    "hacer cara": part_makeface["makeface"],
    "construir cara": part_makeface["makeface"],
    "generar cara": part_makeface["makeface"],
    "makeface": part_makeface["makeface"],
    "createface": part_makeface["createface"],

    "upgrade": part_makeface["upgrade"],
    "actualizar": part_makeface["upgrade"],
    "mejora": part_makeface["upgrade"],
    "promover": part_makeface["upgrade"],

    "ayuda":            part_makeface['help'],
    "información":      part_makeface['help'],
    "opciones":         part_makeface['help']
}

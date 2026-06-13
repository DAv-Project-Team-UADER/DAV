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

"""Spanish spoken-word mapping for Part section commands."""

from .part_section import part_section
from .ayuda import ayuda

TraduceToEs = {
    "seccion": part_section["section"],
    "sección": part_section["section"],
    "crear seccion": part_section["section"],
    "crear sección": part_section["section"],
    "obtener seccion": part_section["section"],
    "obtener sección": part_section["section"],
    "interseccion": part_section["section"],
    "intersección": part_section["section"],
    "curva de seccion": part_section["section"],
    "curva de sección": part_section["section"],
    "corte": part_section["section"],
    "ayuda": ayuda,
    "manual": ayuda,
    "soporte": ayuda,
    "documentacion": ayuda,
    "documentación": ayuda,
    "help": ayuda,
}

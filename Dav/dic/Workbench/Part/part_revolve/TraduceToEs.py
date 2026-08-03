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

"""Spanish spoken-word mapping for the part_revolve dictionary."""

from .part_revolve import part_revolve

from .ayuda import ayuda

TraduceToEs = {
    "revolucion": part_revolve["revolve"],
    "revolución": part_revolve["revolve"],
    "revolucionar": part_revolve["revolve"],
    "crear revolucion": part_revolve["revolve"],
    "crear revolución": part_revolve["revolve"],

    "ayuda": part_revolve['help'],
    "información": part_revolve['help'],
    "opciones": part_revolve['help'],
}


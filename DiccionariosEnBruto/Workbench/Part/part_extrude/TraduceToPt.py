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

"""Portuguese spoken-word mapping for Part extrude commands."""

from .part_extrude import part_extrude
from .ayuda import ayuda

TraduceToPt = {
    "extrudir": part_extrude["extrude"],
    "extrusao": part_extrude["extrude"],
    "extrusão": part_extrude["extrude"],
    "criar extrusao": part_extrude["extrude"],
    "criar extrusão": part_extrude["extrude"],
    "fazer extrusao": part_extrude["extrude"],
    "fazer extrusão": part_extrude["extrude"],
    "extrudir objeto": part_extrude["extrude"],
    "extrude": part_extrude["extrude"],

    "ajuda":             part_extrude["help"],
    "informação":       part_extrude["help"],
    "opções":            part_extrude["help"]
}
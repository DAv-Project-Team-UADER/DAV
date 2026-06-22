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

"""English spoken-word mapping for Part chamfer commands."""

from .part_chamfer import part_chamfer
from .ayuda import ayuda

TraduceToEn = {
    "chamfer": part_chamfer["chaflan"],
    "create chamfer": part_chamfer["chaflan"],
    "make chamfer": part_chamfer["chaflan"],
    "bevel": part_chamfer["chaflan"],
    "create bevel": part_chamfer["chaflan"],
    "make bevel": part_chamfer["chaflan"],

    "help":            part_chamfer['help'],
    "info":            part_chamfer['help'],
    "options":         part_chamfer['help']

}
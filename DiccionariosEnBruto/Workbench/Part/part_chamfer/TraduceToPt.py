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

"""Portuguese spoken-word mapping for Part chamfer commands."""

from .part_chamfer import part_chamfer

from .ayuda import ayuda

TraduceToPt = {
    "chanfro": part_chamfer["chaflan"],
    "chanfrar": part_chamfer["chaflan"],
    "bisel": part_chamfer["chaflan"],
    "biselar": part_chamfer["chaflan"],
    "criar chanfro": part_chamfer["chaflan"],
    "fazer chanfro": part_chamfer["chaflan"],
    "criar bisel": part_chamfer["chaflan"],
    "fazer bisel": part_chamfer["chaflan"],
    "chamfer": part_chamfer["chaflan"],

    "ajuda":             part_chamfer['help'],
    "informação":        part_chamfer['help'],
    "opções":            part_chamfer['help']


}

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

"""Portuguese spoken-word mapping for Part cross sections commands."""

from .part_cross_sections import part_cross_sections

from .ayuda import ayuda

TraduceToPt = {
    "secoes transversais": part_cross_sections["cross sections"],
    "seções transversais": part_cross_sections["cross sections"],
    "secao transversal": part_cross_sections["cross sections"],
    "seção transversal": part_cross_sections["cross sections"],
    "criar secoes transversais": part_cross_sections["cross sections"],
    "criar seções transversais": part_cross_sections["cross sections"],
    "fazer secoes transversais": part_cross_sections["cross sections"],
    "fazer seções transversais": part_cross_sections["cross sections"],
    "secoes": part_cross_sections["cross sections"],
    "seções": part_cross_sections["cross sections"],
    "cross sections": part_cross_sections["cross sections"],

"ajuda":                part_cross_sections['help'],
"informação":          part_cross_sections['help'],
"opções":             part_cross_sections['help']
}

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

"""Portuguese spoken-word mapping for PartDesign modify commands."""

from .modify import modify
from .ayuda import ayuda

TraduceToPt = {
    # Fillet
    "arredondamento": modify["fillet"],
    "arredondar": modify["fillet"],
    "filete": modify["fillet"],

    # Chamfer
    "chanfro": modify["chamfer"],
    "bisel": modify["chamfer"],
    "chanfrar": modify["chamfer"],
    "biselar": modify["chamfer"],

    # Draft
    "inclinação": modify["draft"],
    "inclinar": modify["draft"],
    "conicidade": modify["draft"],
    "conicizar": modify["draft"],

    # Thickness
    "espessura": modify["thickness"],
    "casca": modify["thickness"],
    "adicionar espessura": modify["thickness"],
    "adicionar casca": modify["thickness"],

    # Help
    "ajuda": ayuda,
    "manual": ayuda,
    "suporte": ayuda,
    "documentação": ayuda,
}

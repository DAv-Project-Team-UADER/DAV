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

TraduceToEn = {
    "clone": modify["clone"],
    "copy": modify["clone"],

    "downgrade": modify["downgrade"],
    "simplify": modify["downgrade"],

    "sketch": modify["sketch"],
    "convert to sketch": modify["sketch"],

    "edit": modify["edit"],
    "modify": modify["edit"],

    "fillet": modify["fillet"],
    "round": modify["fillet"],

    "join": modify["join"],
    "combine": modify["join"],

    "move": modify["move"],
    "translate": modify["move"],

    "offset": modify["offset"],
    "parallel copy": modify["offset"],

    "rotate": modify["rotate"],
    "turn": modify["rotate"],

    "mirror": modify["mirror"],
    "reflect": modify["mirror"],

    "help": modify["help"],
    "info": modify["help"],
    "options": modify["help"],
}
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

TraduceToPt = {
    "clonar": modify["clone"],
    "copiar": modify["clone"],

    "simplificar": modify["downgrade"],
    "rebaixar": modify["downgrade"],
    "esboço": modify["sketch"],
    "converter para esboço": modify["sketch"],

    "editar": modify["edit"],
    "modificar": modify["edit"],

    "arredondar": modify["fillet"],
    "filete": modify["fillet"],
    "borda arredondada": modify["fillet"],
    "borda": modify["fillet"],

    "unir": modify["join"],
    "combinar": modify["join"],
    "juntar": modify["join"],
    "junto": modify["join"],
    "realocar": modify["join"],
    "mover": modify["move"],
    "deslocar": modify["move"],
    "deslocamento": modify["offset"],

    "deslocamento": modify["offset"],
    "offset": modify["offset"],

    "rotacionar": modify["rotate"],
    "girar": modify["rotate"],

    "espelhar": modify["mirror"],
    "espelho": modify["mirror"],
    "refletir": modify["mirror"],

    "help": modify["help"],
    "ajuda": modify["help"],
    "opções": modify["help"],
}
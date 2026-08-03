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

"""Mapeamento de comandos falados em português para Tree."""

from .Tree import tree
from .ayuda import ayuda

TraduceToPt = {
    # Comandos de árvore
    "colapsar": tree["collapse"],
    "contrair": tree["collapse"],
    "dobrar": tree["collapse"],

    "preseleção": tree["preselection"],
    "preselecionar": tree["preselection"],
    "pré-seleção": tree["preselection"],

    "registrar seleção": tree["recordselection"],
    "gravar seleção": tree["recordselection"],
    "salvar seleção": tree["recordselection"],

    "expandir individual": tree["singleexpand"],
    "expandir um": tree["singleexpand"],
    "abrir um": tree["singleexpand"],

    "sincronizar posição": tree["syncplacement"],
    "sincronizar posicionamento": tree["syncplacement"],
    "alinhar posição": tree["syncplacement"],

    "sincronizar seleção": tree["syncselection"],
    "sincronizar selecao": tree["syncselection"],
    "combinar seleção": tree["syncselection"],

    "sincronizar vista": tree["syncview"],
    "sincronizar visão": tree["syncview"],
    "combinar vista": tree["syncview"],

    "ajuda": tree["help"],
    "informação": tree["help"],
    "opções": tree["help"],
}
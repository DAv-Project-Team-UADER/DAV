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

# ============================================================
# Traduções para Português – PartDesign (somente pastas)
# ============================================================

from .partdesign import partdesign

TraduceToPt = {

    # Pastas principais
    "base": partdesign["base"],
    "aditivo": partdesign["additive"],
    "subtrativo": partdesign["subtractive"],
    "modificar": partdesign["modify"],
    "transformar": partdesign["transform"],
    "gerenciar": partdesign["manage"],

    # Sinônimos
    "basico": partdesign["base"],
    "fundamental": partdesign["base"],

    "adicionar": partdesign["additive"],
    "acrescentar": partdesign["additive"],
    "adições": partdesign["additive"],

    "subtrair": partdesign["subtractive"],
    "remover": partdesign["subtractive"],
    "cortar": partdesign["subtractive"],

    "editar": partdesign["modify"],
    "edição": partdesign["modify"],
    "modificadores": partdesign["modify"],

    "transformações": partdesign["transform"],
    "padrões": partdesign["transform"],

    "administração": partdesign["manage"],
    "configuração": partdesign["manage"],
    
    "ajuda":             partdesign["help"],
    "informação":       partdesign["help"],
    "opções":            partdesign["help"]
    
}

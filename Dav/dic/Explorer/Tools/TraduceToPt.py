# Copyright (C) 2026 El Equipo del Proyecto DAV
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

from .Tools import tools

TraduceToPt = {
    "medir": tools["measure"],
    "medida": tools["measure"],
    "medir distancia": tools["measure"],
    "medir distância": tools["measure"],

    "esclarecer selecao": tools["clarifyselection"],
    "esclarecer seleção": tools["clarifyselection"],
    "limpar selecao": tools["clarifyselection"],
    "limpar seleção": tools["clarifyselection"],

    "modo demo": tools["demomode"],
    "modo demonstracao": tools["demomode"],
    "modo demonstração": tools["demomode"],

    "personalizar": tools["customize"],
    "customizar": tools["customize"],
    "configuracoes": tools["customize"],
    "configurações": tools["customize"],

    "editar parametros": tools["editparameters"],
    "editar parâmetros": tools["editparameters"],
    "parametros": tools["editparameters"],
    "parâmetros": tools["editparameters"],

    "utilitario de projeto": tools["projectutil"],
    "utilitário de projeto": tools["projectutil"],
    "ferramentas de projeto": tools["projectutil"],

    "ajuda": tools["help"],
    "informação": tools["help"],
    "opções": tools["help"],
}
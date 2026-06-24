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

from .views import views
from .ayuda import ayuda

TraduceToPt = {

    # Vista
    "vista": views["view"],
    "criar vista": views["view"],
    "adicionar vista": views["view"],

    # Vista de detalhe
    "vista de detalhe": views["detailview"],
    "detalhe": views["detailview"],
    "criar detalhe": views["detailview"],

    # Vista quebrada
    "vista quebrada": views["brokenview"],
    "quebra": views["brokenview"],

    # Grupo de recorte
    "grupo de recorte": views["clipgroup"],
    "recorte": views["clipgroup"],
    "criar recorte": views["clipgroup"],

    # Seção complexa
    "seção complexa": views["complexsection"],
    "secao complexa": views["complexsection"],
    "seção": views["complexsection"],
    "secao": views["complexsection"],

    # Vista Draft
    "vista draft": views["draft"],
    "draft": views["draft"],
    "vista esboço": views["draft"],
    "esboço": views["draft"],

    # Vista de planilha
    "planilha": views["spreadsheet"],
    "vista de planilha": views["spreadsheet"],
    "folha de cálculo": views["spreadsheet"],
    "folha de calculo": views["spreadsheet"],

    # Ajuda
    "ajuda": ayuda,
}

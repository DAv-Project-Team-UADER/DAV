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

from .Views import views
from .ayuda import ayuda

TraduceToEs = {

    # Vista
    "vista": views["view"],
    "crear vista": views["view"],
    "agregar vista": views["view"],

    # Vista de detalle
    "vista de detalle": views["detailview"],
    "detalle": views["detailview"],
    "crear detalle": views["detailview"],

    # Vista interrumpida
    "vista interrumpida": views["brokenview"],
    "vista rota": views["brokenview"],
    "rotura": views["brokenview"],

    # Grupo de recorte
    "grupo de recorte": views["clipgroup"],
    "recorte": views["clipgroup"],
    "crear recorte": views["clipgroup"],

    # Sección compleja
    "sección compleja": views["complexsection"],
    "seccion compleja": views["complexsection"],
    "sección": views["complexsection"],
    "seccion": views["complexsection"],

    # Vista Draft
    "vista draft": views["draft"],
    "draft": views["draft"],
    "vista boceto": views["draft"],
    "boceto": views["draft"],

    # Vista de hoja de cálculo
    "hoja de cálculo": views["spreadsheet"],
    "hoja de calculo": views["spreadsheet"],
    "vista de hoja de cálculo": views["spreadsheet"],
    "vista de hoja de calculo": views["spreadsheet"],
    "planilla": views["spreadsheet"],

    # Ayuda
    "ayuda": views["help"],
    "información": views["help"],
    "opciones": views["help"],
}

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

TraduceToEn = {

    # View
    "view": views["view"],
    "create view": views["view"],
    "new view": views["view"],

    # Detail View
    "detail view": views["detailview"],
    "detail": views["detailview"],
    "create detail view": views["detailview"],

    # Broken View
    "broken view": views["brokenview"],
    "break view": views["brokenview"],
    "create broken view": views["brokenview"],

    # Clip Group
    "clip group": views["clipgroup"],
    "clipping group": views["clipgroup"],
    "create clip group": views["clipgroup"],

    # Complex Section
    "complex section": views["complexsection"],
    "section view": views["complexsection"],
    "create section": views["complexsection"],

    # Draft View
    "draft view": views["draft"],
    "draft": views["draft"],
    "create draft view": views["draft"],

    # Spreadsheet View
    "spreadsheet view": views["spreadsheet"],
    "spreadsheet": views["spreadsheet"],
    "table view": views["spreadsheet"],

    "help": views["help"],
    "info": views["help"],
    "options": views["help"],
}

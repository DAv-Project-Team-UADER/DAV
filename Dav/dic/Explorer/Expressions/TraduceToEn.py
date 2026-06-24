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


from .Expressions import expressions

TraduceToEn = {
    "copy active document": expressions["copyactdoc"],
    "copy document": expressions["copyactdoc"],

    "copy all documents": expressions["copyalldoc"],
    "copy all": expressions["copyalldoc"],

    "copy selected": expressions["copyselected"],
    "copy selection": expressions["copyselected"],

    "paste expression": expressions["pasteexpr"],
    "paste expressions": expressions["pasteexpr"],

    "help": expressions["help"],
    "info": expressions["help"],
    "options": expressions["help"],
}

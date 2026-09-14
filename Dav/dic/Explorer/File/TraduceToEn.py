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

from .File import file

TraduceToEn = {
    "new": file["new"],
    "new file": file["new"],
    "create": file["new"],
    "create file": file["new"],

    "open": file["open"],
    "open file": file["open"],

    "save": file["save"],
    "save file": file["save"],

    "save as": file["saveas"],
    "save document as": file["saveas"],

    "save copy": file["savecopy"],
    "duplicate file": file["savecopy"],

    "revert": file["revert"],
    "restore": file["revert"],

    "merge": file["merge"],
    "merge projects": file["merge"],

    "import": file["import"],
    "import file": file["import"],

    "export": file["export"],
    "export file": file["export"],

    "recent": file["recent"],
    "recent files": file["recent"],

    "load image": file["loadimage"],
    "open image": file["loadimage"],

    "help": file["help"],
    "info": file["help"],
    "options": file["help"],
}

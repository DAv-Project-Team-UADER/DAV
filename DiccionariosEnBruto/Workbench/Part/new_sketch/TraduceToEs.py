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

"""Spanish spoken-word mapping for Part new sketch commands."""

from .new_sketch import new_sketch
from .ayuda import ayuda

TraduceToEs = {
    "boceto": new_sketch["new sketch"],
    "nuevo boceto": new_sketch["new sketch"],
    "crear boceto": new_sketch["new sketch"],
    "hacer boceto": new_sketch["new sketch"],
    "croquis": new_sketch["new sketch"],
    "nuevo croquis": new_sketch["new sketch"],
    "crear croquis": new_sketch["new sketch"],
    "hacer croquis": new_sketch["new sketch"],
    "sketch": new_sketch["new sketch"],
    "nuevo sketch": new_sketch["new sketch"],
    "crear sketch": new_sketch["new sketch"],
    "hacer sketch": new_sketch["new sketch"],
    "ayuda": ayuda,
    "manual": ayuda,
    "soporte": ayuda,
    "documentacion": ayuda,
    "documentación": ayuda,
    "help": ayuda,
}
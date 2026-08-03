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

"""Mapeo de comandos hablados en español para Tree."""

from .Tree import tree
from .ayuda import ayuda

TraduceToEs = {
    "colapsar": tree["collapse"],
    "contraer": tree["collapse"],
    "plegar": tree["collapse"],

    "preseleccion": tree["preselection"],
    "preseleccionar": tree["preselection"],
    "vista previa": tree["preselection"],

    "registrar seleccion": tree["recordselection"],
    "registrar selección": tree["recordselection"],
    "guardar selección": tree["recordselection"],

    "expandir individual": tree["singleexpand"],
    "expandir uno": tree["singleexpand"],
    "abrir uno": tree["singleexpand"],

    "sincronizar posicion": tree["syncplacement"],
    "sincronizar posición": tree["syncplacement"],
    "alinear posición": tree["syncplacement"],

    "sincronizar seleccion": tree["syncselection"],
    "sincronizar selección": tree["syncselection"],
    "coincidir selección": tree["syncselection"],

    "sincronizar vista": tree["syncview"],
    "sincronizar vista": tree["syncview"],
    "coincidir vista": tree["syncview"],

    "ayuda": tree["help"],
    "información": tree["help"],
    "opciones": tree["help"],
}
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

"""English spoken-word mapping for the Sketcher line geometry dictionary."""

from .line import line
from .ayuda import ayuda

TraduceToEn = {
    
    # Line creation & synonyms
    "create": line['create'],
    "create line": line['create'],
    "draw line": line['create'],
    "line": line['create'],
    "sketch line": line['create'],

    # Line by dictated coordinates & synonyms
    "line by points": line['create_by_points'],
    "create line by points": line['create_by_points'],
    "draw line by points": line['create_by_points'],
    "line by coordinates": line['create_by_points'],

    "help": line['help'],
    "info": line['help'],
    "options": line['help'],
}
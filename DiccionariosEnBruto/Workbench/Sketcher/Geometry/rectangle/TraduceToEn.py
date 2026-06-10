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

"""English spoken-word mapping for the Sketcher rectangle geometry dictionary."""

from .rectangle import rectangle
from .ayuda import ayuda

TraduceToEn = {
    # Help command
    "help": ayuda,
    "info": ayuda,
    
    # Standard rectangle creation & synonyms
    "create": rectangle['create'],
    "create_rectangle": rectangle['create'],
    "draw_rectangle": rectangle['create'],
    "rectangle": rectangle['create'],
    "box": rectangle['create'],
    
    # Centered rectangle creation & synonyms
    "center": rectangle['center'],
    "center_rectangle": rectangle['center'],
    "centered_rectangle": rectangle['center'],
    "create_centered_rectangle": rectangle['center']
}
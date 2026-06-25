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

"""English spoken-word mapping for the Sketcher select dictionary."""

from .select import select
from .ayuda import ayuda

TraduceToEn = {
    
    # Horizontal axis selection & synonyms
    "horizontal": select['horizontal'],
    "horizontal axis": select['horizontal'],
    "select horizontal": select['horizontal'],
    
    # Vertical axis selection & synonyms
    "vertical": select['vertical'],
    "vertical axis": select['vertical'],
    "select vertical": select['vertical'],
    
    # Origin selection & synonyms
    "origin": select['origin'],
    "center point": select['origin'],
    "select origin": select['origin'],
    "zero point": select['origin'],

    "help": select['help'],
    "info": select['help'],
    "options": select['help'],
}
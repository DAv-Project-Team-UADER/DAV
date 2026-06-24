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

"""Spanish spoken-word mapping for the Sketcher select dictionary."""

from .select import select
from .ayuda import ayuda

TraduceToEs = {
    # Comando de ayuda
    "ayuda": ayuda,
    "info": ayuda,
    
    # Eje horizontal y sinónimos
    "horizontal": select['horizontal'],
    "eje horizontal": select['horizontal'],
    "seleccionar eje horizontal": select['horizontal'],
    
    # Eje vertical y sinónimos
    "vertical": select['vertical'],
    "eje vertical": select['vertical'],
    "seleccionar eje vertical": select['vertical'],
    
    # Origen y sinónimos
    "origen": select['origin'],
    "centro": select['origin'],
    "punto central": select['origin'],
    "seleccionar origen": select['origin']
}
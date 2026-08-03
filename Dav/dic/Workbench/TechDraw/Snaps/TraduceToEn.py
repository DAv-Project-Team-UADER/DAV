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


from .Snaps import snaps
from .ayuda import ayuda

TraduceToEn = {

    # Midpoints
    "midpoint": snaps["midpoints"],
    "midpoints": snaps["midpoints"],
    "middle point": snaps["midpoints"],
    "center point": snaps["midpoints"],

    # Quadrants
    "quadrant": snaps["quadrants"],
    "quadrants": snaps["quadrants"],
    "quarter point": snaps["quadrants"],
    "quadrant point": snaps["quadrants"],

    "help": snaps["help"],
    "info": snaps["help"],
    "options": snaps["help"],
}

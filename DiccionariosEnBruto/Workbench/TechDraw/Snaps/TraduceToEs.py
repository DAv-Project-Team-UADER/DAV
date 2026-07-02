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

"""Mapeo de palabras en español para TechDraw Snaps."""

from .Snaps import snaps
from .ayuda import ayuda

TraduceToEs = {

    # Puntos medios
    "puntos medios": snaps["midpoints"],
    "punto medio": snaps["midpoints"],
    "medio": snaps["midpoints"],
    "centro de arista": snaps["midpoints"],

    # Cuadrantes
    "cuadrantes": snaps["quadrants"],
    "cuadrante": snaps["quadrants"],
    "puntos cuadrantes": snaps["quadrants"],

    # Ayuda
    "ayuda": snaps["help"],
    "información": snaps["help"],
    "opciones": snaps["help"],
}

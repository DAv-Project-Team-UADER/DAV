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

"""Mapeo de palabras en español para TechDraw Hatching."""

from .hatching import hatching
from .ayuda import ayuda

TraduceToEs = {

    # Rayado geométrico
    "rayado": hatching["geometric_hatch"],
    "rayado geométrico": hatching["geometric_hatch"],
    "tramado": hatching["geometric_hatch"],
    "relleno": hatching["geometric_hatch"],
    "relleno geométrico": hatching["geometric_hatch"],
    "trama": hatching["geometric_hatch"],
    "trama geométrica": hatching["geometric_hatch"],
    "patrón de rayado": hatching["geometric_hatch"],
    "patron de rayado": hatching["geometric_hatch"],
    "patrón de tramado": hatching["geometric_hatch"],
    "patron de tramado": hatching["geometric_hatch"],

    # Ayuda
    "ayuda": ayuda,
}

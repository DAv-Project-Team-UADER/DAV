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

"""English spoken-word mapping for PartDesign subtractive commands."""

from .subtractive import subtractive
from .ayuda import ayuda

TraduceToEn = {
    # Pocket
    "pocket": subtractive["pocket"],
    "cut": subtractive["pocket"],

    # Groove
    "groove": subtractive["groove"],
    "slot": subtractive["groove"],

    # Hole
    "hole": subtractive["hole"],
    "drill": subtractive["hole"],

    # Subtractive primitives
    "subtractivebox": subtractive["subtractivebox"],
    "cutbox": subtractive["subtractivebox"],

    "subtractivecone": subtractive["subtractivecone"],
    "cutcone": subtractive["subtractivecone"],

    "subtractivecylinder": subtractive["subtractivecylinder"],
    "cutcylinder": subtractive["subtractivecylinder"],

    "subtractiveellipsoid": subtractive["subtractiveellipsoid"],
    "cutellipsoid": subtractive["subtractiveellipsoid"],

    "subtractivehelix": subtractive["subtractivehelix"],
    "cuthelix": subtractive["subtractivehelix"],

    "subtractiveloft": subtractive["subtractiveloft"],
    "cutloft": subtractive["subtractiveloft"],

    "subtractivepipe": subtractive["subtractivepipe"],
    "cutpipe": subtractive["subtractivepipe"],

    "subtractiveprism": subtractive["subtractiveprism"],
    "cutprism": subtractive["subtractiveprism"],

    "subtractivesphere": subtractive["subtractivesphere"],
    "cutsphere": subtractive["subtractivesphere"],

    "subtractivetorus": subtractive["subtractivetorus"],
    "cuttorus": subtractive["subtractivetorus"],

    "subtractivewedge": subtractive["subtractivewedge"],
    "cutwedge": subtractive["subtractivewedge"],

    # Boolean
    "boolean": subtractive["boolean"],
    "booleanoperation": subtractive["boolean"],
    "booleanop": subtractive["boolean"],

    # Help
    "help": ayuda,
    "manual": ayuda,
    "support": ayuda,
    "documentation": ayuda,
}

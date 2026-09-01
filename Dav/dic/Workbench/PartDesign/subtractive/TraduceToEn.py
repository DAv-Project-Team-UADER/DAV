
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
from measure import CreateDimension

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

    # Subtractive Box
    "subtractivebox": subtractive["subtractivebox"],
    "cutbox": subtractive["subtractivebox"],

    # Subtractive Cone
    "subtractivecone": subtractive["subtractivecone"],
    "cutcone": subtractive["subtractivecone"],

    # Subtractive Cylinder
    "subtractivecylinder": subtractive["subtractivecylinder"],
    "cutcylinder": subtractive["subtractivecylinder"],

    # Subtractive Ellipsoid
    "subtractiveellipsoid": subtractive["subtractiveellipsoid"],
    "cutellipsoid": subtractive["subtractiveellipsoid"],

    # Subtractive Helix
    "subtractivehelix": subtractive["subtractivehelix"],
    "cuthelix": subtractive["subtractivehelix"],

    # Subtractive Loft
    "subtractiveloft": subtractive["subtractiveloft"],
    "cutloft": subtractive["subtractiveloft"],

    # Subtractive Pipe
    "subtractivepipe": subtractive["subtractivepipe"],
    "cutpipe": subtractive["subtractivepipe"],

    # Subtractive Prism
    "subtractiveprism": subtractive["subtractiveprism"],
    "cutprism": subtractive["subtractiveprism"],

    # Subtractive Sphere
    "subtractivesphere": subtractive["subtractivesphere"],
    "cutsphere": subtractive["subtractivesphere"],

    # Subtractive Torus
    "subtractivetorus": subtractive["subtractivetorus"],
    "cuttorus": subtractive["subtractivetorus"],

    # Subtractive Wedge
    "subtractivewedge": subtractive["subtractivewedge"],
    "cutwedge": subtractive["subtractivewedge"],

    # Boolean
    "boolean": subtractive["boolean"],
    "booleanoperation": subtractive["boolean"],
    "booleanop": subtractive["boolean"],

    # Cuts by dictated measure (no dialog)
    "pocket by length":      subtractive["pocket_by_length"],
    "hollow by length":      subtractive["pocket_by_length"],

    "hole by size":          subtractive["hole_by_size"],
    "drill by size":         subtractive["hole_by_size"],

    "groove by angle":       subtractive["groove_by_angle"],

    # Primitive cuts by dictated measures
    "cut box by size":       subtractive["cut_box_by_size"],
    "cut cylinder by size":  subtractive["cut_cylinder_by_size"],
    "cut sphere by radius":  subtractive["cut_sphere_by_radius"],

    # Help
    "help": subtractive['help'],
    "info": subtractive['help'],
    "options": subtractive['help'],

    # MEASURE
    "measure": CreateDimension,
    "measure distance": CreateDimension,
    "distance": CreateDimension,
    "dimension": CreateDimension,
    "dimensioning": CreateDimension,
    "meter": CreateDimension,
    "milimeter": CreateDimension,
    "millimeter": CreateDimension,
    "centimeter": CreateDimension,
    "tape measure": CreateDimension,
    "tape tool": CreateDimension,
    "tape": CreateDimension,
    "ruler": CreateDimension,
}
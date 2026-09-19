
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
    "blind hole":            subtractive["blind_hole"],
    "blind hole by size":    subtractive["blind_hole"],
    "blind drill":           subtractive["blind_hole"],

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

from dic.StdView.StandardViews.StandardViews import *

TraduceToEn.update ({
    # Bottom
    'bottom': StandardViews['bottom'],
    'below': StandardViews['bottom'],
    'down': StandardViews['bottom'],
    'lower': StandardViews['bottom'],

    # Top
    'top': StandardViews['top'],
    'above': StandardViews['top'],
    'upper': StandardViews['top'],

    # Front
    'front': StandardViews['front'],
    'forward': StandardViews['front'],

    # Rear
    'rear': StandardViews['rear'],
    'back': StandardViews['rear'],
    'behind': StandardViews['rear'],

    # Left
    'left': StandardViews['left'],

    # Right
    'right': StandardViews['right'],

    # Isometric
    'isometric': StandardViews['isometric'],
    'iso': StandardViews['isometric'],

    # Dimetric
    'dimetric': StandardViews['dimetric'],

    # Trimetric
    'trimetric': StandardViews['trimetric'],

    # Fit All
    'fit all': StandardViews['fitall'],
    'fit': StandardViews['fitall'],
    'fitview': StandardViews['fitall'],
    'zoomfit': StandardViews['fitall'],

    # Fit Selection
    'fit selection': StandardViews['fitselection'],
    'fit selected': StandardViews['fitselection'],
    'zoom selection': StandardViews['fitselection'],

    # Zoom in
    'zoom in': StandardViews['zoomin'],
    'zoom in view': StandardViews['zoomin'],

    # Zoom out
    'zoom out': StandardViews['zoomout'],
    'zoom out view': StandardViews['zoomout'],

    # Box Zoom
    'box zoom': StandardViews['boxzoom'],
    'window zoom': StandardViews['boxzoom'],
    'zoom window': StandardViews['boxzoom'],

    # New View
    'new view': StandardViews['newview'],
    'create view': StandardViews['newview'],

    # Home
    'home': StandardViews['home'],
    'default view': StandardViews['home'],
    'reset view': StandardViews['home'],

    # Fullscreen
    'full screen': StandardViews['fullscreen'],
    'full screenmode': StandardViews['fullscreen'],

})

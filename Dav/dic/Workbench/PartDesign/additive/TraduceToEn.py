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
from .additive import additive
from .ayuda import ayuda
from measure import CreateDimension

TraduceToEn = {
    # Pad
    "pad": additive["pad"],
    "pad feature": additive["pad"],
    "extrude": additive["pad"],
    "extrusion": additive["pad"],

    # Revolution
    "revolution": additive["revolution"],
    "revolution feature": additive["revolution"],

    # AdditiveHelix
    "additive helix": additive["additivehelix"],
    "Coil feature": additive["additivehelix"],

    # AdditiveLoft
    "additive loft": additive["additiveloft"],
    "loft feature": additive["additiveloft"],

    # AdditivePipe
    "additive pipe": additive["additivepipe"],
    "pipe feature": additive["additivepipe"],

    # AdditiveBox
    "additive box": additive["additivebox"],
    "box": additive["additivebox"],
    "Additive solid box": additive["additivebox"],

    # AdditiveCone
    "additive cone": additive["additivecone"],
    "cone": additive["additivecone"],
    "cone feature": additive["additivecone"],

    # AdditiveCylinder
    "additive cylinder": additive["additivecylinder"],
    "cylinder": additive["additivecylinder"],
    "cylinder feature": additive["additivecylinder"],

    # AdditiveEllipsoid
    "additive ellipsoid": additive["additiveellipsoid"],
    "ellipsoid feature": additive["additiveellipsoid"],

    # AdditivePrism
    "additive prism": additive["additiveprism"],
    "prism": additive["additiveprism"],
    "prism feature": additive["additiveprism"],

    # AdditiveSphere
    "additive sphere": additive["additivesphere"],
    "sphere feature": additive["additivesphere"],

    # AdditiveTorus
    "additive torus": additive["additivetorus"],
    "torus feature": additive["additivetorus"],
    
    # AdditiveWedge
    "additive wedge": additive["additivewedge"],
    "wedge feature": additive["additivewedge"],
    
    # pad_sketch
    "extrude sketch": additive["pad_sketch"],
    "extend profile": additive["pad_sketch"],
    "thicken drawing": additive["pad_sketch"],

    # loft_profiles
    "blend shapes": additive["loft_profiles"],
    "sweep surfaces": additive["loft_profiles"],
    "morph sections": additive["loft_profiles"],



    # Pad by dictated length (no dialog)
    "pad by length": additive["pad_by_length"],
    "extrude by length": additive["pad_by_length"],
    "extrude by height": additive["pad_by_length"],
    "give height": additive["pad_by_length"],

    # Box by dictated dimensions
    "box by size": additive["box_by_size"],
    "cube by size": additive["box_by_size"],
    "create box by size": additive["box_by_size"],
    "box by dimensions": additive["box_by_size"],

    # Cylinder by dictated dimensions
    "cylinder by size": additive["cylinder_by_size"],
    "create cylinder by size": additive["cylinder_by_size"],
    "cylinder by radius and height": additive["cylinder_by_size"],

    # Revolution by dictated angle
    "revolution by angle": additive["revolve_by_angle"],
    "revolve by angle": additive["revolve_by_angle"],
    "spin profile": additive["revolve_by_angle"],

    # Primitives by dictated measures
    "sphere by radius":      additive["sphere_by_radius"],
    "cone by size":          additive["cone_by_size"],
    "torus by size":         additive["torus_by_size"],
    "prism by size":         additive["prism_by_size"],

    "help":            additive['help'],
    "info":            additive['help'],
    "options":         additive['help']
,
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
    'left view': StandardViews['left'],
    'left side': StandardViews['left'],
    'from the left': StandardViews['left'],
    'view from the left': StandardViews['left'],

    # Right
    'right': StandardViews['right'],
    'right view': StandardViews['right'],
    'right side': StandardViews['right'],
    'from the right': StandardViews['right'],
    'view from the right': StandardViews['right'],

    # Isometric
    'isometric': StandardViews['isometric'],
    'iso': StandardViews['isometric'],

    # Dimetric
    'dimetric': StandardViews['dimetric'],
    'dimetric view': StandardViews['dimetric'],
    'dimetric projection': StandardViews['dimetric'],
    'dimetric perspective': StandardViews['dimetric'],

    # Trimetric
    'trimetric': StandardViews['trimetric'],
    'trimetric view': StandardViews['trimetric'],
    'trimetric projection': StandardViews['trimetric'],
    'trimetric perspective': StandardViews['trimetric'],

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

# Mover la vista (centra la cámara en un punto)
from moveview import MoveView, MOVE_VIEW_PHRASES
for _phrase in MOVE_VIEW_PHRASES['en']:
    TraduceToEn.setdefault(_phrase, MoveView)

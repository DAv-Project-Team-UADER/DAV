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

"""English spoken-word mapping for the DAV AssemblyWorkbench dictionary."""
 
from .Assembly import assembly
from .joint.joint import joint
from .ayuda import ayuda
 
TraduceToEn = {
    "new assembly":      assembly["create"],
    "create assembly":   assembly["create"],
    "new part":          assembly["newpart"],
    "insert part":       assembly["newpart"],
    "insert link":       assembly["link"],
    "link part":         assembly["link"],
    "solve":             assembly["solve"],
    "solve assembly":    assembly["solve"],
    "exploded view":     assembly["view"],
    "create view":       assembly["view"],
    "simulation":        assembly["simulation"],
    "create simulation": assembly["simulation"],
    "bill of materials": assembly["bom"],
    "bom":               assembly["bom"],
    "preferences":       assembly["preferences"],
    "settings":          assembly["preferences"],
    "ground":            assembly["grounded"],
    "toggle grounded":   assembly["grounded"],
    "joint":             joint,
    
    # Voice joints (no dialog)
    "fixed joint":           assembly["fixed_joint"],
    "lock parts":            assembly["fixed_joint"],

    "revolute joint":        assembly["revolute_joint"],
    "hinge":                 assembly["revolute_joint"],

    "slider joint":          assembly["slider_joint"],
    "slide parts":           assembly["slider_joint"],

    "distance joint":        assembly["distance_joint"],
    "hold apart":            assembly["distance_joint"],

    "angle joint":           assembly["angle_joint"],
    "angle between parts":   assembly["angle_joint"],

    "ground part":           assembly["ground_part"],
    "anchor part":           assembly["ground_part"],

    # Remaining voice joints
    "ball joint":            assembly["ball_joint"],
    "cylindrical joint":     assembly["cylindrical_joint"],
    "cylinder joint":        assembly["cylindrical_joint"],
    "parallel joint":        assembly["parallel_joint"],
    "keep parallel":         assembly["parallel_joint"],
    "perpendicular joint":   assembly["perpendicular_joint"],
    "keep perpendicular":    assembly["perpendicular_joint"],

    "gears joint":           assembly["gears_joint"],
    "mesh gears":            assembly["gears_joint"],
    "belt joint":            assembly["belt_joint"],
    "screw joint":           assembly["screw_joint"],
    "rack and pinion joint": assembly["rack_pinion_joint"],

    "help":            joint['help'],
    "info":            joint['help'],
    "options":         joint['help']
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

    # Help
    "help":            StandardViews['help'],
    "info":            StandardViews['help'],
    "options":         StandardViews['help']
})

# Cota / medir
from measure import CreateDimension, MEASURE_PHRASES
for _phrase in MEASURE_PHRASES['en']:
    TraduceToEn.setdefault(_phrase, CreateDimension)

# Mover la vista (centra la cámara en un punto)
from moveview import MoveView, MOVE_VIEW_PHRASES
for _phrase in MOVE_VIEW_PHRASES['en']:
    TraduceToEn.setdefault(_phrase, MoveView)

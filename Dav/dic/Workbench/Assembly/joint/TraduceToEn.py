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

"""English spoken-word mapping for the DAV joint dictionary."""

from .joint import joint
from .ayuda import ayuda

TraduceToEn = {

    # Angle
    "angle joint": joint["angle"],
    "angle": joint["angle"],

    # Ball
    "ball joint": joint["ball"],
    "ball": joint["ball"],
    "sphere joint": joint["ball"],
    "sphere": joint["ball"],

    # Parallel
    "parallel joint": joint["parallel"],
    "parallel": joint["parallel"],

    # Perpendicular
    "perpendicular joint": joint["perpendicular"],
    "perpendicular": joint["perpendicular"],

    # Belt
    "belt joint": joint["belt"],
    "belt": joint["belt"],
    "chain joint": joint["belt"],
    "chain": joint["belt"],

    # Gear
    "gear joint": joint["gears"],
    "gear": joint["gears"],
    "gears": joint["gears"],

    # Rack and pinion
    "rack pinion": joint["rackpinion"],
    "rack and pinion": joint["rackpinion"],
    "rack pinion joint": joint["rackpinion"],
    "rack and pinion joint": joint["rackpinion"],

    # Screw
    "screw joint": joint["screw"],
    "screw": joint["screw"],
    "lead screw": joint["screw"],

    # Cylindrical
    "cylindrical joint": joint["cylindrical"],
    "cylindrical": joint["cylindrical"],

    # Distance
    "distance joint": joint["distance"],
    "distance": joint["distance"],

    # Fixed
    "fixed joint": joint["fixed"],
    "fixed": joint["fixed"],

    # Revolute
    "revolute joint": joint["revolute"],
    "revolute": joint["revolute"],

    # Slider
    "slider joint": joint["slider"],
    "slider": joint["slider"],

    # Help
    "help": joint["help"],
    "info": joint["help"],
    "options": joint["help"]
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

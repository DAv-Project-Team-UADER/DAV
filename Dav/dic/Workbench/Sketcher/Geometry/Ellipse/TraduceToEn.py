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

# ============================================================
# English translations – Sketcher Ellipse
# ============================================================

from ._ellipse import ellipse

TraduceToEn = {
    # Main commands (now parametric with window) — digit + word for Vosk
    "center": ellipse["center"],
    "3points": ellipse["3points"],
    "3 points": ellipse["3points"],
    "three points": ellipse["3points"],
    "three point": ellipse["3points"],
    "elliptic": ellipse["elliptic"],
    "hyperbolic": ellipse["hyperbolic"],
    "parabolic": ellipse["parabolic"],

    # Aliases
    "ellipse center": ellipse["center"],
    "ellipse 3 points": ellipse["3points"],
    "ellipse three points": ellipse["3points"],
    "ellipse arc": ellipse["elliptic"],
    "hyperbola arc": ellipse["hyperbolic"],
    "parabola arc": ellipse["parabolic"],

    "help": ellipse["help"],
    "info": ellipse["help"],
    "options": ellipse["help"],

    # Ellipse by dictated coordinates (window like line by points)
    "ellipse by center": ellipse['create_by_center'],
    "create ellipse by center": ellipse['create_by_center'],
    "ellipse by radii": ellipse['create_by_center'],
    "ellipse by coordinates": ellipse['create_by_center'],

    "ellipse by three points": ellipse['create_by_3_points'],
    "create ellipse by three points": ellipse['create_by_3_points'],
    "ellipse by 3 points": ellipse['create_by_3_points'],
    "elliptic arc by coordinates": ellipse['create_elliptic'],
    "hyperbolic arc by coordinates": ellipse['create_hyperbolic'],
    "parabolic arc by coordinates": ellipse['create_parabolic'],
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

# Cota / medir
from measure import CreateDimension, MEASURE_PHRASES
for _phrase in MEASURE_PHRASES['en']:
    TraduceToEn.setdefault(_phrase, CreateDimension)

# Mover la vista (centra la cámara en un punto)
from moveview import MoveView, MOVE_VIEW_PHRASES
for _phrase in MOVE_VIEW_PHRASES['en']:
    TraduceToEn.setdefault(_phrase, MoveView)

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

"""English spoken-word mapping for the DAV StdView dictionary folders."""

from .StdView import StdView

from .Appearance.Appearance import appearance
from .Camera.Camera import camera
from .Clipping.Clipping import clipping
from .DrawStyles.DrawStyles import drawstyles
from .Material.Material import material
from .Overlay.Overlay import overlay
from .Panels.Panels import Panels
from .SavedViews.SavedViews import savedviews
from .StandardViews.StandardViews import StandardViews
from .Stereo.Stereo import stereo
from .Toolbars.Toolbars import toolbars
from .Tree.Tree import tree
from .Visibility.Visibility import visibility
from .ayuda import ayuda
from measure import CreateDimension

TraduceToEn = {
    "appearance": StdView["appearance"],
    "visual appearance": StdView["appearance"],
    "look": StdView["appearance"],

    "camera": StdView["camera"],
    "view camera": StdView["camera"],

    "clipping": StdView["clipping"],
    "clip": StdView["clipping"],
    "clipping plane": StdView["clipping"],

    "draw styles": StdView["drawstyles"],
    "drawing styles": StdView["drawstyles"],
    "display styles": StdView["drawstyles"],
    "visual styles": StdView["drawstyles"],

    "material": StdView["material"],
    "materials": StdView["material"],

    "overlay": StdView["overlay"],
    "overlays": StdView["overlay"],
    "overlay view": StdView["overlay"],

    "panels": StdView["panels"],
    "panel": StdView["panels"],
    "view panels": StdView["panels"],

    "saved views": StdView["savedviews"],
    "saved view": StdView["savedviews"],
    "bookmarked views": StdView["savedviews"],

    "standard views": StdView["standardviews"],
    "standard view": StdView["standardviews"],
    "basic views": StdView["standardviews"],

    "stereo": StdView["stereo"],
    "stereoscopic": StdView["stereo"],
    "stereo view": StdView["stereo"],

    "toolbars": StdView["toolbars"],
    "toolbar": StdView["toolbars"],
    "view toolbars": StdView["toolbars"],

    "tree": StdView["tree"],
    "model tree": StdView["tree"],
    "document tree": StdView["tree"],

    "visibility": StdView["visibility"],
    "visible": StdView["visibility"],
    "show hide": StdView["visibility"],

    "help": StdView["help"],
    "info": StdView["help"],
    "options": StdView["help"],

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

    # Help
    "help":            StandardViews['help'],
    "info":            StandardViews['help'],
    "options":         StandardViews['help']
})

# Mover la vista (centra la cámara en un punto)
from moveview import MoveView, MOVE_VIEW_PHRASES
for _phrase in MOVE_VIEW_PHRASES['en']:
    TraduceToEn.setdefault(_phrase, MoveView)

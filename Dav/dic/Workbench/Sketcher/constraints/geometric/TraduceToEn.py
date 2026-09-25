# Copyright (C) 2026 El Equipo del Proyecto DAV
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

"""English spoken-word mapping for the geometric dictionary."""

from .geometric import geometric

TraduceToEn = {
    # Apunta a los elementos del diccionario original 'geometric'
    'coincident':           geometric['coincident'],
    'make coincident':      geometric['coincident'],
    'join points':          geometric['coincident'],

    'coincident unified':   geometric['coincidentunified'],
    'unified coincident':   geometric['coincidentunified'],

    'lock':                 geometric['lock'],
    'fix position':         geometric['lock'],

    'point on object':      geometric['pointonobject'],
    'fix to line':          geometric['pointonobject'],

    'horizontal':           geometric['horizontal'],
    'make horizontal':      geometric['horizontal'],
    
    'vertical':             geometric['vertical'],
    'make vertical':        geometric['vertical'],
    
    'horizontal vertical':  geometric['horver'],
    'auto orientation':     geometric['horver'],

    'parallel':             geometric['parallel'],
    'make parallel':        geometric['parallel'],
    
    'perpendicular':        geometric['perpendicular'],
    'make perpendicular':   geometric['perpendicular'],

    'tangent':              geometric['tangent'],
    'make tangent':         geometric['tangent'],

    'equal':                geometric['equal'],
    'make equal':           geometric['equal'],
    'equal length':         geometric['equal'],

    'symmetric':            geometric['symmetric'],
    'make symmetric':       geometric['symmetric'],
    'symmetry':             geometric['symmetric'],
    'aplicate symmetry':             geometric['symmetric'],

    'block':                geometric['block'],
    'block geometry':       geometric['block'],

    'toggle driving':       geometric['toggledriving'],
    'reference mode':       geometric['toggledriving'],
    'driving mode':         geometric['toggledriving'],

    'toggle active':        geometric['toggleactive'],
    'activate constraint':  geometric['toggleactive'],
    'deactivate constraint':geometric['toggleactive'],

    # Sinónimos para la función ayuda
    'help':                 geometric['help'],
    'info':             geometric['help'],
    'options':              geometric['help']
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

# Cota / medir
from measure import CreateDimension, MEASURE_PHRASES
for _phrase in MEASURE_PHRASES['en']:
    TraduceToEn.setdefault(_phrase, CreateDimension)

# Mover la vista (centra la cámara en un punto)
from moveview import MoveView, MOVE_VIEW_PHRASES
for _phrase in MOVE_VIEW_PHRASES['en']:
    TraduceToEn.setdefault(_phrase, MoveView)

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

"""English spoken-word mapping for the Sketcher tools dictionary."""

from .tools import tools
from .ayuda import ayuda
from measure import CreateDimension

TraduceToEn = {
    
    # Delete constraints & synonyms
    "deleteconstraints": tools['deleteconstraints'],
    "delete constraints": tools['deleteconstraints'],
    "clear constraints": tools['deleteconstraints'],
    "remove constraints": tools['deleteconstraints'],
    
    # Delete geometry & synonyms
    "deletegeometry": tools['deletegeometry'],
    "delete geometry": tools['deletegeometry'],
    "clear geometry": tools['deletegeometry'],
    "clear sketch": tools['deletegeometry'],
    "close sketch": tools['leave'],
    "leave sketch": tools['leave'],
    "exit sketch": tools['leave'],
    "finish sketch": tools['leave'],
    "erase sketch": tools['deletegeometry'],
    
    # Merge & synonyms
    "merge": tools['merge'],
    "merge sketches": tools['merge'],
    "combine sketches": tools['merge'],
    
    # Reorient & synonyms
    "reorient": tools['reorient'],
    "reorient sketch": tools['reorient'],
    "change sketch plane": tools['reorient'],
    
    # Remove axes alignment & synonyms
    "removeaxes": tools['removeaxes'],
    "remove axes": tools['removeaxes'],
    "clear axes alignment": tools['removeaxes'],

    "help": tools['help'],
    "info": tools['help'],
    "options": tools['help']
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

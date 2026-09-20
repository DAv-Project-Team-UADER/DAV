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

"""English spoken-word mapping for the circle dictionary."""

from .circle import circle

TraduceToEn = {
    # Apunta a los elementos del diccionario original 'circle'
    'create':           circle['create'],
    'circle':           circle['create'],
    'center circle':    circle['create'],
    'circle by center': circle['create'],

    'three point':      circle['3point'],
    'three points':     circle['3point'],
    '3 point':          circle['3point'],
    '3 points':         circle['3point'],
    'circle by 3 points': circle['3point'],

    # Sinónimos para la función ayuda
    'help':             circle['help'],
    'info':         circle['help'],
    'options':          circle['help'],

    # Circle by dictated coordinates
    "circle by center": circle['create_by_center'],
    "create circle by center": circle['create_by_center'],
    "circle by radius": circle['create_by_center'],
    "circle by coordinates": circle['create_by_center'],

    # Circle by 3 points — new parametric with 6 floats + optional label
    "circle by three points": circle['create_by_3_points'],
    "create circle by three points": circle['create_by_3_points'],
    "circle by 3 points": circle['create_by_3_points'],
    "create circle by 3 points": circle['create_by_3_points'],
    'circle by parameters':             circle['create_by_center_radius'],
    'circle by center and radius':      circle['create_by_center_radius'],
    'parametric three point circle':    circle['create_by_3points'],
    'three points parametric':          circle['create_by_3points'],
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

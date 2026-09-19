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

"""English spoken-word mapping for TechDraw workbench dictionary."""

from .TechDraw import techdraw

TraduceToEn = {
    # TechDraw submenus
    "views":                  techdraw["views"],
    "drawing views":          techdraw["views"],

    "dimensions":             techdraw["dimensions"],
    "dimension":              techdraw["dimensions"],
    "measurements":           techdraw["dimensions"],

    "lines":                  techdraw["addlines"],
    "add lines":              techdraw["addlines"],

    "symbols":                techdraw["symbols"],
    "symbol":                 techdraw["symbols"],

    "snaps":                  techdraw["snaps"],
    "snap":                   techdraw["snaps"],

    "topology":               techdraw["topology"],

    "page":                   techdraw["page"],
    "sheet":                  techdraw["page"],
    "drawing sheet":          techdraw["page"],

    "annotations":            techdraw["annotations"],
    "notes":                  techdraw["annotations"],

    "hatching":               techdraw["hatching"],
    "hatch":                  techdraw["hatching"],

    "vertices":               techdraw["addvertices"],
    "add vertices":           techdraw["addvertices"],

    "other views":            techdraw["otherviews"],
    "auxiliary views":        techdraw["otherviews"],

    "features":               techdraw["features"],

    "help":                   techdraw["help"],
    "info":                   techdraw["help"],
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

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

"""English spoken-word mapping for the Sketcher workbench."""

from .sketcher import sketcher as Sketcher
import FreeCADGui as Gui

# Importaciones relativas porque estamos en la misma carpeta
from .sketcher import _toggle_construction
from .ayuda import ayuda as sketcher_ayuda
from .sketcher import sketcher
from measure import CreateDimension

TraduceToEn = {

    # Carpetas de Sketcher
    "geometry": sketcher["geometry"],
    "geometric": sketcher["geometry"],

    "arcslot": sketcher["arcslot"],
    "arcs": sketcher["arcslot"],
    "arc": sketcher["arcslot"],
    
    "constraints": sketcher["constraints"],
    "constraint": sketcher["constraints"],
    "restrictions": sketcher["constraints"],
    
    "external": sketcher["external"],
    
    "oblong": sketcher["oblong"],
    "create oblong": sketcher["oblong"],
    
    "point": sketcher["point"],
    "create point": sketcher["point"],
    
    "select": sketcher["select"],
    "selection": sketcher["select"],
    
    "slot": sketcher["slot"],
    "create slot": sketcher["slot"],
    
    "square": sketcher["square"],
    "create square": sketcher["square"],
    "draw square": sketcher["square"],
    
    "text": sketcher["text"],
    "write text": sketcher["text"],
    "create text": sketcher["text"],
    
    "tools": sketcher["tools"],
    "tool": sketcher["tools"],
    
    "triangle": sketcher["triangle"],
    "create triangle": sketcher["triangle"],
    "draw triangle": sketcher["triangle"],
    
    "validate": sketcher["validate"],
    "validate sketch": sketcher["validate"],
    
    "view": sketcher["view"],
    "view sketch": sketcher["view"],
    "view selection": sketcher["view"],
    
    # --- Traducciones de la parte inferior de sketcher.py ---
    
    # Control del Boceto / Sketch
    "new": sketcher["new"],
    "new sketch": sketcher["new"],
    "create sketch": sketcher["new"],

    "edit": sketcher["edit"],
    "edit sketch": sketcher["edit"],
    "modify sketch": sketcher["edit"],

    "attach": sketcher["attach"],
    "map sketch": sketcher["attach"],
    "attach sketch": sketcher["attach"],

    "grid": sketcher["grid"],
    "toggle grid": sketcher["grid"],
    "show grid": sketcher["grid"],

    "close sketch": sketcher["leave"],
    "leave sketch": sketcher["leave"],
    "exit sketch": sketcher["leave"],
    "finish sketch": sketcher["leave"],

    "cancelediting": sketcher["cancelediting"],
    "cancel editing": sketcher["cancelediting"],
    "stop editing": sketcher["cancelediting"],

    # Geometría de Construcción
    "toggleconstruction": _toggle_construction,
    "toggle construction": _toggle_construction,
    "construction mode": _toggle_construction,

    # Edición y Portapapeles
    "carboncopy": sketcher["carboncopy"],
    "carbon copy": sketcher["carboncopy"],

    "copyelements": sketcher["copyelements"],
    "copy elements": sketcher["copyelements"],
    "copy geometry": sketcher["copyelements"],

    "cutelements": sketcher["cutelements"],
    "cut elements": sketcher["cutelements"],
    "cut geometry": sketcher["cutelements"],

    "pasteelements": sketcher["pasteelements"],
    "paste elements": sketcher["pasteelements"],
    "paste geometry": sketcher["pasteelements"],

    # Transformaciones y Modificaciones
    "mirror": sketcher["mirror"],
    "symmetry": sketcher["mirror"],
    "mirror elements": sketcher["mirror"],

    "mirrorsketch": sketcher["mirrorsketch"],
    "mirror sketch": sketcher["mirrorsketch"],

    "offset": sketcher["offset"],
    "create offset": sketcher["offset"],

    "movearray": sketcher["movearray"],
    "translate": sketcher["movearray"],
    "move elements": sketcher["movearray"],

    "rotatepolar": sketcher["rotatepolar"],
    "rotate": sketcher["rotatepolar"],
    "rotate elements": sketcher["rotatepolar"],

    "scale": sketcher["scale"],
    "scale elements": sketcher["scale"],

    # Operaciones de Bordes / Esquinas
    "trimedge": sketcher["trimedge"],
    "trim": sketcher["trimedge"],
    "trim edge": sketcher["trimedge"],

    "splitedge": sketcher["splitedge"],
    "split": sketcher["splitedge"],
    "split edge": sketcher["splitedge"],

    "extendedge": sketcher["extendedge"],
    "extend": sketcher["extendedge"],
    "extend edge": sketcher["extendedge"],

    "fillet": sketcher["fillet"],
    "create fillet": sketcher["fillet"],

    "chamfer": sketcher["chamfer"],
    "create chamfer": sketcher["chamfer"],

    # Soporte y Ayuda
    "help": Sketcher['help'],
    "info": Sketcher['help'],
    "options": Sketcher['help'],

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

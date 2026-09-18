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

from .selection import selection
from .ayuda import ayuda

TraduceToEn = {
    # next
    "advance": selection["next"],
    "forward": selection["next"],
    "skip": selection["next"],
    "next": selection["next"],
    "next object": selection["next"],
    "next item": selection["next"],
    "select next": selection["next"],
    "select next object": selection["next"],
    "object next": selection["next"],

    # previous
    "back": selection["previous"],
    "go back": selection["previous"],
    "previous": selection["previous"],
    "previous object": selection["previous"],
    "previous item": selection["previous"],
    "select previous": selection["previous"],
    "select previous object": selection["previous"],
    "object previous": selection["previous"],

    # selectall
    "all": selection["selectall"],
    "everything": selection["selectall"],
    "select all": selection["selectall"],
    "select all objects": selection["selectall"],
    "select everything": selection["selectall"],

    # deselectall
    "none": selection["deselectall"],
    "nothing": selection["deselectall"],
    "remove": selection["deselectall"],
    "uncheck": selection["deselectall"],
    "uncheck all": selection["deselectall"],
    "deselect": selection["deselectall"],
    "deselect all": selection["deselectall"],
    "clear selection": selection["deselectall"],
    "unselect": selection["deselectall"],
    "clear": selection["deselectall"],

    # current
    "which": selection["current"],
    "this": selection["current"],
    "current": selection["current"],
    "current object": selection["current"],
    "which object": selection["current"],

    # count
    "how many": selection["count"],
    "count": selection["count"],
    "how many objects": selection["count"],

    # delete — remove the currently selected object (next/previous + delete)
    "delete": selection["delete"],
    "delete object": selection["delete"],
    "delete element": selection["delete"],
    "delete selection": selection["delete"],
    "remove object": selection["delete"],
    "remove": selection["delete"],
    "erase": selection["delete"],
    "erase object": selection["delete"],
    "suppress": selection["delete"],

    "help": ayuda,
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
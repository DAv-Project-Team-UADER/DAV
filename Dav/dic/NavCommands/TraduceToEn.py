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

"""English spoken-word mapping for Browser navigation commands."""

from .NavActions import NavActions

TraduceToEn = {
    # Go up one level
    "up":             NavActions["up"],
    "go up":          NavActions["up"],
    "back":           NavActions["up"],
    "go back":        NavActions["up"],
    "return":         NavActions["up"],
    "exit":           NavActions["up"],

    # Show the active context
    "context":        NavActions["show_context"],
    "where am i":     NavActions["show_context"],
    "what can i say": NavActions["show_context"],
    "available options": NavActions["show_context"],
    "show context":   NavActions["show_context"],
    "location":       NavActions["show_context"],

    # Confirm the dictated phrase
    "send":           NavActions["send"],
    "enter":          NavActions["send"],
    "accept":         NavActions["send"],
    "confirm":        NavActions["send"],
    "ok":             NavActions["send"],
    "okey":           NavActions["send"],
    "okay":           NavActions["send"],
    "done":           NavActions["send"],
    "yes":            NavActions["send"],
    "yep":            NavActions["send"],

    # Discard the phrase in progress
    "cancel":         NavActions["cancel"],
    "discard":        NavActions["cancel"],
    "never mind":     NavActions["cancel"],
    "abort":          NavActions["cancel"],
    "no":             NavActions["cancel"],
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
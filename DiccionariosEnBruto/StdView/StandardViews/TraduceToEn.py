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

import FreeCADGui as Gui

from .ayuda import ayuda

from .StandardViews import StandardViews

TranslateToEn = {
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
    'fitall': StandardViews['fitall'],
    'fit': StandardViews['fitall'],
    'fitview': StandardViews['fitall'],
    'zoomfit': StandardViews['fitall'],

    # Fit Selection
    'fitselection': StandardViews['fitselection'],
    'fitselected': StandardViews['fitselection'],
    'zoomselection': StandardViews['fitselection'],

    # Zoom in
    'zoomin': StandardViews['zoomin'],
    'zoominview': StandardViews['zoomin'],

    # Zoom out
    'zoomout': StandardViews['zoomout'],
    'zoomoutview': StandardViews['zoomout'],

    # Box Zoom
    'boxzoom': StandardViews['boxzoom'],
    'windowzoom': StandardViews['boxzoom'],
    'zoomwindow': StandardViews['boxzoom'],

    # New View
    'newview': StandardViews['newview'],
    'createview': StandardViews['newview'],

    # Home
    'home': StandardViews['home'],
    'defaultview': StandardViews['home'],
    'resetview': StandardViews['home'],

    # Fullscreen
    'fullscreen': StandardViews['fullscreen'],
    'fullscreenmode': StandardViews['fullscreen'],

    # Help
    'help': StandardViews['help'],
    'assist': StandardViews['help'],
    'manual': StandardViews['help'],
}

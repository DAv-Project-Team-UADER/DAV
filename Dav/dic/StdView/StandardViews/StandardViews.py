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
from pivy import coin

from .ayuda import ayuda

ZOOM_STEP = 1.1


def _apply_zoom(factor):
    """Apply zoom by modifying camera height/focalDistance by *factor*.

    ``factor < 1`` zooms in (view gets closer), ``factor > 1`` zooms out.
    Works for both orthographic and perspective cameras.
    """
    view = Gui.ActiveDocument.ActiveView
    if view is None:
        return
    cam = view.getCameraNode()
    if cam is None:
        return
    if isinstance(cam, coin.SoOrthographicCamera):
        cam.height = cam.height.getValue() * factor
    else:
        direction = coin.SbVec3f()
        cam.orientation.getValue().multVec(coin.SbVec3f(0, 0, -1), direction)
        old_focal = cam.focalDistance.getValue()
        new_focal = old_focal * factor
        cam.position = cam.position.getValue() + (new_focal - old_focal) * (-direction)
        cam.focalDistance = new_focal


def _zoom_in():
    _apply_zoom(1.0 / ZOOM_STEP)


def _zoom_out():
    _apply_zoom(ZOOM_STEP)


# Diccionario DAV - StdView / StandardViews
StandardViews = {
    'bottom':       lambda: Gui.runCommand('Std_ViewBottom', 0),
    'boxzoom':      lambda: Gui.runCommand('Std_ViewBoxZoom', 0),
    'newview':      lambda: Gui.runCommand('Std_ViewCreate', 0),
    'dimetric':     lambda: Gui.runCommand('Std_ViewDimetric', 0),
    'fitall':       lambda: Gui.runCommand('Std_ViewFitAll', 0),
    'fitselection': lambda: Gui.runCommand('Std_ViewFitSelection', 0),
    'front':        lambda: Gui.runCommand('Std_ViewFront', 0),
    'fullscreen':   lambda: Gui.runCommand('Std_ViewFullscreen', 0),
    'home':         lambda: Gui.runCommand('Std_ViewHome', 0),
    'isometric':    lambda: Gui.runCommand('Std_ViewIsometric', 0),
    'left':         lambda: Gui.runCommand('Std_ViewLeft', 0),
    'rear':         lambda: Gui.runCommand('Std_ViewRear', 0),
    'right':        lambda: Gui.runCommand('Std_ViewRight', 0),
    'top':          lambda: Gui.runCommand('Std_ViewTop', 0),
    'trimetric':    lambda: Gui.runCommand('Std_ViewTrimetric', 0),
    'zoomin':       _zoom_in,
    'zoomout':      _zoom_out,
    'help':         ayuda,
}
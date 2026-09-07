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

ZOOM_FACTOR = 0.9  # 10% de variación


def _apply_zoom(factor):
    """Apply zoom by directly modifying the active 3D view camera node.

    Args:
        factor (float): Multiplier for zoom. < 1 zooms in (closer), > 1 zooms out (farther).
    """
    view = getattr(Gui.ActiveDocument, 'ActiveView', None) if getattr(Gui, 'ActiveDocument', None) else None
    if view is None and hasattr(Gui, 'activeView'):
        view = Gui.activeView()
    if view is None:
        return

    cam = view.getCameraNode()
    if cam is None:
        return

    # Cámara Ortográfica (modo por defecto de FreeCAD)
    if hasattr(cam, 'height'):
        cam.height.setValue(cam.height.getValue() * factor)
    # Cámara Perspectiva
    elif hasattr(cam, 'position') and hasattr(cam, 'focalDistance'):
        direction = view.getViewDirection()
        old_focal = cam.focalDistance.getValue()
        new_focal = old_focal * factor
        delta = old_focal - new_focal  # positivo al acercar (factor < 1)

        pos = cam.position.getValue()
        new_pos = [
            pos[0] + delta * direction.x,
            pos[1] + delta * direction.y,
            pos[2] + delta * direction.z,
        ]
        cam.position.setValue(new_pos)
        cam.focalDistance.setValue(new_focal)

    view.redraw()


def _zoom_in():
    """Acercar la cámara un 10%."""
    _apply_zoom(ZOOM_FACTOR)


def _zoom_out():
    """Alejar la cámara un 10%."""
    _apply_zoom(1.0 / ZOOM_FACTOR)

def _toggle_fullscreen():
    """Alterna el modo de pantalla completa de la ventana principal."""
    try:
        Gui.runCommand('Std_MainFullscreen', 0)
    except Exception:
        mw = Gui.getMainWindow()
        if mw:
            if mw.isFullScreen():
                mw.showNormal()
            else:
                mw.showFullScreen()




# Diccionario DAV - StdView / StandardViews
StandardViews = {
    'bottom':       lambda: Gui.runCommand('Std_ViewBottom', 0),
    'boxzoom':      lambda: Gui.runCommand('Std_ViewBoxZoom', 0),
    'newview':      lambda: Gui.runCommand('Std_ViewCreate', 0),
    'dimetric':     lambda: Gui.runCommand('Std_ViewDimetric', 0),
    'fitall':       lambda: Gui.runCommand('Std_ViewFitAll', 0),
    'fitselection': lambda: Gui.runCommand('Std_ViewFitSelection', 0),
    'front':        lambda: Gui.runCommand('Std_ViewFront', 0),
    'fullscreen':   _toggle_fullscreen,
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
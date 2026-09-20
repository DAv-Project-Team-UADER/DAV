#  Copyright (C) 2026 The DAV Project Team
#  Copyright (C) 2026 El Equipo del Proyecto DAV
#  Universidad Autónoma de Entre Ríos (UADER)
#  Directed by Gerard Guillermo and Gallo Fabricio David
#  Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, in GPLv3 version of the License
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <https://www.gnu.org/licenses/>.
#  SPDX-License-Identifier: GPL-3.0-or-later

"""Move the view: center the camera on a dictated point ("mover").

Pide un punto y desplaza la cámara hasta que la vista queda centrada en él,
sin cambiar hacia dónde mira ni el zoom. Igual que la cota, decide si el
punto es plano (X, Y) o espacial (X, Y, Z) según el documento (ver
``measure.dimensionMode``).
"""

import inspect

import FreeCAD as App

from measure import dimensionMode

try:
    import FreeCADGui as Gui
except ImportError:  # sin interfaz no hay vista que mover
    Gui = None


def _centerViewOn(point) -> bool:
    """Slide the active camera so that ``point`` is at the centre of the view.

    Args:
        point: ``App.Vector`` in global coordinates.

    Returns:
        True when the camera was moved.
    """
    try:
        view = Gui.ActiveDocument.ActiveView
        from pivy import coin

        camera = view.getCameraNode()
        # la cámara mira a lo largo de su eje -Z: se retrocede desde el punto la
        # distancia de enfoque, así la orientación y el zoom no cambian
        look = camera.orientation.getValue().multVec(coin.SbVec3f(0.0, 0.0, -1.0)).getValue()
        distance = camera.focalDistance.getValue()
        camera.position.setValue(
            coin.SbVec3f(
                point.x - look[0] * distance,
                point.y - look[1] * distance,
                point.z - look[2] * distance,
            )
        )
    except Exception as error:
        print(f"[DAV] No se pudo mover la vista: {error}")
        return False
    return True


def _move3d(x: float, y: float, z: float):
    """Center the view on the point (x, y, z)."""
    if _centerViewOn(App.Vector(float(x), float(y), float(z))):
        print(f"[DAV] Vista centrada en ({x}, {y}, {z}).")


def _move2d(x: float, y: float):
    """Center the view on the point (x, y) of the drawing plane."""
    _mode, sketch = dimensionMode()
    point = App.Vector(float(x), float(y), 0.0)
    if sketch is not None:
        # dentro de un boceto el punto está en las coordenadas del boceto
        point = sketch.Placement.multVec(point)
    if _centerViewOn(point):
        print(f"[DAV] Vista centrada en ({x}, {y}).")


class _MoveView:
    """Voice command that asks for 2 or 3 values depending on the document.

    Mismo mecanismo que ``CreateDimension``: la firma se calcula al ejecutar,
    así el colector de parámetros abre dos o tres ventanas según el caso.
    """

    __name__ = "MoveView"

    @property
    def __signature__(self):
        mode, _sketch = dimensionMode()
        return inspect.signature(_move2d if mode == "2D" else _move3d)

    def __call__(self, *args, **kwargs):
        is3d = "z" in kwargs or len(args) == 3
        if not kwargs and not args:
            is3d = dimensionMode()[0] == "3D"
        return (_move3d if is3d else _move2d)(*args, **kwargs)


MoveView = _MoveView()

# Frases habladas por idioma. Cada TraduceTo las agrega con setdefault: donde
# «mover» ya significa otra cosa (mover elementos, mover un objeto) esa gana, y
# quedan sinónimos que no chocan con nada: «centrar», «ir a», «panear», «mover vista»...
MOVE_VIEW_PHRASES = {
    "es": (
        "mover", "mover vista", "mover camara", "mover cámara", "desplazar vista",
        "arrastrar vista", "centrar en", "centrar vista", "ir a punto", "ir al punto",
        "centrar", "panear", "ir a", "llevar a", "posicionar vista",
    ),
    "en": (
        "move", "move view", "move camera", "pan", "pan view", "drag view",
        "center on", "center view", "go to point",
        "shift", "go to", "navigate to", "reposition view",
    ),
    "pt": (
        "mover", "mover vista", "mover camera", "mover câmera", "deslocar vista",
        "arrastar vista", "centralizar em", "centrar vista", "ir ao ponto",
        "centralizar", "ir para", "levar a", "posicionar vista",
    ),
}

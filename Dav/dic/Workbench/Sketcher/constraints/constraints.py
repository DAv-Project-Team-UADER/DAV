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

import Sketcher
from .common import GetActiveSketch, RequireGeometry, TryAddConstraint, Finish
from .ayuda import ayuda
from .geometric.geometric import geometric


def _apply(constraint_type, args, min_geom, hint, label):
    """Apply a dimensional Sketcher constraint to the active sketch.

    Args:
        constraint_type: Sketcher.Constraint type string (e.g. 'Distance').
        args: Tuple of positional arguments passed after the type string.
        min_geom: Minimum number of geometry elements required.
        hint: Spanish description of required geometry shown on error.
        label: Label printed on success.
    """
    doc, sketch = GetActiveSketch()
    if doc and sketch and RequireGeometry(sketch, min_geom, hint):
        TryAddConstraint(sketch, Sketcher.Constraint(constraint_type, *args))
        Finish(doc, label)


def set_dimension(value: float):
    _apply('Distance', (0, 1, 0, 2, value), 1, 'una línea', 'Dimension')


def set_horizontal(value: float):
    _apply('DistanceX', (0, 1, 0, 2, value), 1, 'una línea', 'Horizontal Dimension')


def set_vertical(value: float):
    _apply('DistanceY', (0, 1, 0, 2, value), 1, 'una línea', 'Vertical Dimension')


def set_angle(value: float):
    _apply('Angle', (0, 1, value), 2, 'dos líneas', 'Angle Dimension')


def set_radius(value: float):
    _apply('Radius', (0, value), 1, 'un arco o círculo', 'Radius Dimension')


def set_diameter(value: float):
    _apply('Diameter', (0, value), 1, 'un círculo', 'Diameter Dimension')


def set_distance(value: float):
    _apply('Distance', (0, 1, 0, 2, value), 1, 'una línea', 'Distance Dimension')


constraints = {
    'dimension': set_dimension,
    'horizontal': set_horizontal,
    'vertical': set_vertical,
    'angle': set_angle,
    'radius': set_radius,
    'diameter': set_diameter,
    'radiam': set_diameter,
    'distance': set_distance,
    'geometric': geometric,
    'help': ayuda,
}

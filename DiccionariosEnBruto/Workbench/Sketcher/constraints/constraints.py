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


constraints = {
    'dimension':  lambda: _apply('Distance',   (0, 1, 0, 2, 15.0),  1, 'una línea',           'Dimension'),
    'horizontal': lambda: _apply('DistanceX',  (0, 1, 0, 2, 18.0),  1, 'una línea',           'Horizontal Dimension'),
    'vertical':   lambda: _apply('DistanceY',  (0, 1, 0, 2, 20.0),  1, 'una línea',           'Vertical Dimension'),
    'angle':      lambda: _apply('Angle',      (0, 1, 45.0),         2, 'dos líneas',           'Angle Dimension'),
    'radius':     lambda: _apply('Radius',     (0, 10.0),            1, 'un arco o círculo',   'Radius Dimension'),
    'diameter':   lambda: _apply('Diameter',   (0, 14.0),            1, 'un círculo',          'Diameter Dimension'),
    'radiam':     lambda: _apply('Diameter',   (0, 14.0),            1, 'un círculo',          'Radius/Diameter Dimension'),
    'distance':   lambda: _apply('Distance',   (0, 1, 0, 2, 20.0),  1, 'una línea',           'Distance Dimension'),
    'geometric':  geometric,
    'help':       ayuda,
}

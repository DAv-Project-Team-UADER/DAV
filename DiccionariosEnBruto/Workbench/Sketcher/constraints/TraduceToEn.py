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

"""English spoken-word mapping for the constraints dictionary."""

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


TraduceToEn = {
    # Cota genérica de distancia
    'dimension':            lambda: _apply('Distance',  (0, 1, 0, 2, 15.0),  1, 'una línea',            'Dimension'),
    'add dimension':        lambda: _apply('Distance',  (0, 1, 0, 2, 15.0),  1, 'una línea',            'Dimension'),
    'length':               lambda: _apply('Distance',  (0, 1, 0, 2, 15.0),  1, 'una línea',            'Dimension'),

    # Distancia horizontal
    'horizontal':           lambda: _apply('DistanceX', (0, 1, 0, 2, 18.0),  1, 'una línea',            'Horizontal Dimension'),
    'horizontal dimension': lambda: _apply('DistanceX', (0, 1, 0, 2, 18.0),  1, 'una línea',            'Horizontal Dimension'),
    'horizontal distance':  lambda: _apply('DistanceX', (0, 1, 0, 2, 18.0),  1, 'una línea',            'Horizontal Dimension'),

    # Distancia vertical
    'vertical':             lambda: _apply('DistanceY', (0, 1, 0, 2, 20.0),  1, 'una línea',            'Vertical Dimension'),
    'vertical dimension':   lambda: _apply('DistanceY', (0, 1, 0, 2, 20.0),  1, 'una línea',            'Vertical Dimension'),
    'vertical distance':    lambda: _apply('DistanceY', (0, 1, 0, 2, 20.0),  1, 'una línea',            'Vertical Dimension'),

    # Ángulo
    'angle':                lambda: _apply('Angle',     (0, 1, 45.0),        2, 'dos líneas',           'Angle Dimension'),
    'angle dimension':      lambda: _apply('Angle',     (0, 1, 45.0),        2, 'dos líneas',           'Angle Dimension'),

    # Radio
    'radius':               lambda: _apply('Radius',    (0, 10.0),           1, 'un arco o círculo',    'Radius Dimension'),
    'radius dimension':     lambda: _apply('Radius',    (0, 10.0),           1, 'un arco o círculo',    'Radius Dimension'),

    # Diámetro
    'diameter':             lambda: _apply('Diameter',  (0, 14.0),           1, 'un círculo',           'Diameter Dimension'),
    'diameter dimension':   lambda: _apply('Diameter',  (0, 14.0),           1, 'un círculo',           'Diameter Dimension'),

    # Radio / Diámetro (automático de ticket)
    'radiam':               lambda: _apply('Diameter',  (0, 14.0),           1, 'un círculo',           'Radius/Diameter Dimension'),
    'auto dimension':       lambda: _apply('Diameter',  (0, 14.0),           1, 'un círculo',           'Radius/Diameter Dimension'),

    # Distancia específica
    'distance':             lambda: _apply('Distance',  (0, 1, 0, 2, 20.0),  1, 'una línea',            'Distance Dimension'),
    'distance dimension':   lambda: _apply('Distance',  (0, 1, 0, 2, 20.0),  1, 'una línea',            'Distance Dimension'),

    # Subconjunto geométrico
    'geometric':            geometric,
    'geometric constraints':geometric,
    'geometry constraints': geometric,

    # Comandos de ayuda
    'help':                 ayuda,
    'commands':             ayuda,
    'options':              ayuda
}

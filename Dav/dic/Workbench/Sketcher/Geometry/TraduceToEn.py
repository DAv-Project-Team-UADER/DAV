# Copyright (C) 2026 El Equipo del Proyecto DAV
# Copyright (C) 2026 The DAV Project Team
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

"""English spoken-word mapping for the Sketcher Geometry dictionary."""

from .geometry import geometry
from measure import CreateDimension

TraduceToEn = {
    # Geometry submenus
    "line":                   geometry["line"],
    "straight line":          geometry["line"],

    "polyline":               geometry["polyline"],
    "multi line":             geometry["polyline"],

    "rectangle":              geometry["rectangle"],
    "box":                    geometry["rectangle"],

    "circle":                 geometry["circle"],

    "arc":                    geometry["arc"],

    "arc slot":               geometry["arc_slot"],

    "ellipse":                geometry["ellipse"],

    "polygon":                geometry["polygon"],

    "hexagon":                geometry["hexagon"],

    "heptagon":               geometry["heptagon"],

    "bspline":                geometry["bspline"],
    "spline":                 geometry["bspline"],

    "tools":                  geometry["tools"],
    "bspline tools":          geometry["tools"],

    # Sketch controls
    "new":                    geometry["new"],
    "new sketch":             geometry["new"],
    "create sketch":          geometry["new"],

    "edit":                   geometry["edit"],
    "edit sketch":            geometry["edit"],

    "attach":                 geometry["attach"],
    "map sketch":             geometry["attach"],

    "grid":                   geometry["grid"],

    "stop":                   geometry["stop"],

    "leave":                  geometry["leave"],
    "exit sketch":            geometry["leave"],

    "help":                   geometry["help"],
    "info":                   geometry["help"],
    "options":                geometry["help"],

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
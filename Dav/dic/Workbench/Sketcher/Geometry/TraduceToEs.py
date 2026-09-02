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

"""Spanish spoken-word mapping for the Sketcher Geometry dictionary."""

from .geometry import geometry
from measure import CreateDimension

TraduceToEs = {
    # Submenús de figuras
    "linea":              geometry["line"],
    "línea":              geometry["line"],
    "recta":              geometry["line"],

    "polilinea":          geometry["polyline"],
    "polilínea":          geometry["polyline"],
    "linea multiple":     geometry["polyline"],

    "rectangulo":         geometry["rectangle"],
    "rectángulo":         geometry["rectangle"],

    "circulo":            geometry["circle"],
    "círculo":            geometry["circle"],

    "arco":               geometry["arc"],

    "ranura de arco":     geometry["arc_slot"],
    "arco ranurado":      geometry["arc_slot"],

    "elipse":             geometry["ellipse"],
    "ovalo":              geometry["ellipse"],
    "óvalo":              geometry["ellipse"],

    "poligono":           geometry["polygon"],
    "polígono":           geometry["polygon"],

    "hexagono":           geometry["hexagon"],
    "hexágono":           geometry["hexagon"],

    "heptagono":          geometry["heptagon"],
    "heptágono":          geometry["heptagon"],

    "bspline":            geometry["bspline"],
    "curva bspline":      geometry["bspline"],
    "spline":             geometry["bspline"],

    "herramientas":       geometry["tools"],
    "herramientas bspline": geometry["tools"],

    # Control del boceto
    "nuevo":              geometry["new"],
    "nuevo croquis":      geometry["new"],
    "crear croquis":      geometry["new"],

    "editar":             geometry["edit"],
    "editar croquis":     geometry["edit"],

    "adjuntar":           geometry["attach"],
    "mapear croquis":     geometry["attach"],

    "cuadricula":         geometry["grid"],
    "cuadrícula":         geometry["grid"],

    "ayuda":              geometry["help"],
    "información":        geometry["help"],
    "opciones":           geometry["help"],

    # MEASURE
    "medir": CreateDimension,
    "medir distancia": CreateDimension,
    "acotar": CreateDimension,
    "dimensionar": CreateDimension,
    "cotar": CreateDimension,
    "distancia": CreateDimension,
    "medida": CreateDimension,
    "longitud": CreateDimension,
    "separación": CreateDimension,
    "separacion": CreateDimension,
    "cota": CreateDimension,
    "acotación": CreateDimension,
    "acotacion": CreateDimension,
    "dimensión": CreateDimension,
    "dimension": CreateDimension,
    "métrica": CreateDimension,
    "metrica": CreateDimension,
    "metro": CreateDimension,
    "milímetro": CreateDimension,
    "milimetro": CreateDimension,
    "centímetro": CreateDimension,
    "centimetro": CreateDimension,
    "cinta": CreateDimension,
    "flexómetro": CreateDimension,
    "flexometro": CreateDimension,
    "metro enrollable": CreateDimension,
    "regla": CreateDimension,
    "escalímetro": CreateDimension,
    "escalimetro": CreateDimension,
    "calibre": CreateDimension,
    "pie de rey": CreateDimension,
    "línea de cota": CreateDimension,
    "linea de cota": CreateDimension,
    "cota lineal": CreateDimension,
    "acotación lineal": CreateDimension,
    "acotacion lineal": CreateDimension,
    "dimensionado": CreateDimension,
    "micrómetro": CreateDimension,
    "micrometro": CreateDimension,
}
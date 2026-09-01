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

from .subtractive import subtractive
from .ayuda import ayuda
from measure import CreateDimension

TraduceToEs = {
    # Pocket
    "vaciado": subtractive["pocket"],
    "corte": subtractive["pocket"],

    # Groove
    "ranura": subtractive["groove"],
    "canal": subtractive["groove"],

    # Hole
    "agujero": subtractive["hole"],
    "orificio": subtractive["hole"],

    # Subtractive Box
    "caja sustractiva": subtractive["subtractivebox"],

    # Subtractive Cone
    "cono sustractivo": subtractive["subtractivecone"],

    # Subtractive Cylinder
    "cilindro sustractivo": subtractive["subtractivecylinder"],

    # Subtractive Ellipsoid
    "elipsoide sustractivo": subtractive["subtractiveellipsoid"],

    # Subtractive Helix
    "helice sustractiva": subtractive["subtractivehelix"],

    # Subtractive Loft
    "recubrimiento sustractivo": subtractive["subtractiveloft"],

    # Subtractive Pipe
    "tuberia sustractiva": subtractive["subtractivepipe"],

    # Subtractive Prism
    "prisma sustractivo": subtractive["subtractiveprism"],

    # Subtractive Sphere
    "esfera sustractiva": subtractive["subtractivesphere"],

    # Subtractive Torus
    "toro sustractivo": subtractive["subtractivetorus"],

    # Subtractive Wedge
    "cuna sustractiva": subtractive["subtractivewedge"],

    # Boolean
    "booleano": subtractive["boolean"],
    "operacion booleana": subtractive["boolean"],

    # Help
    "ayuda": subtractive['help'],
    "información": subtractive['help'],
    "opciones": subtractive['help'],

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
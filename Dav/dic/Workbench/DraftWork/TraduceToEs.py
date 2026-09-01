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

from .DraftWork import draft
from .ayuda import ayuda
from measure import CreateDimension

TraduceToEs = {
    'anotacion':  draft['annotation'],
    'anotación':  draft['annotation'],
    'nota':       draft['annotation'],
    'texto':      draft['annotation'],

    'arco':       draft['arc'],

    'curva':      draft['curve'],
    'spline':     draft['curve'],

    'circulo':    draft['circle'],
    'círculo':    draft['circle'],

    'matriz':     draft['array'],
    'patron':     draft['array'],
    'patrón':     draft['array'],
    'matriz circular': draft['array'],

    'modificar':  draft['modify'],
    'editar':     draft['modify'],
    'cambiar':    draft['modify'],

    'dimension':  draft['dimension'],
    'dimensión':  draft['dimension'],
    'medida':     draft['dimension'],
    'medir':      draft['dimension'],

    'elipse':     draft['ellipse'],
    'ovalo':      draft['ellipse'],
    'óvalo':      draft['ellipse'],

    'aglutinante': draft['facebinder'],
    'unir caras': draft['facebinder'],
    'union de caras': draft['facebinder'],

    'colocacion de puntos': draft['pointplacement'],
    'colocación de puntos': draft['pointplacement'],
    'punto especifico':    draft['pointplacement'],
    'punto específico':    draft['pointplacement'],

    'conectar puntos': draft['pointconnect'],
    'conexion de puntos': draft['pointconnect'],
    'conexión de puntos': draft['pointconnect'],

    "ayuda":                draft["help"],
    "información":          draft["help"],
    "opciones":             draft["help"]

,
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
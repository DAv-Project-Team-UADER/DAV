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

"""Portuguese spoken-word mapping for the Sketcher Geometry dictionary."""

from .geometry import geometry
from measure import CreateDimension

TraduceToPt = {
    # Submenús e geometrias
    "linha":                  geometry["line"],
    "reta":                   geometry["line"],

    "polinha":                geometry["polyline"],
    "polilinha":              geometry["polyline"],

    "retângulo":              geometry["rectangle"],
    "retangulo":              geometry["rectangle"],

    "círculo":                geometry["circle"],
    "circulo":                geometry["circle"],

    "arco":                   geometry["arc"],

    "ranura de arco":         geometry["arc_slot"],

    "elipse":                 geometry["ellipse"],

    "polígono":               geometry["polygon"],
    "poligono":               geometry["polygon"],

    "hexágono":               geometry["hexagon"],
    "hexagono":               geometry["hexagon"],

    "heptágono":              geometry["heptagon"],
    "heptagono":              geometry["heptagon"],

    "bspline":                geometry["bspline"],
    "spline":                 geometry["bspline"],

    "ferramentas":            geometry["tools"],

    # Controle do esboço
    "novo":                   geometry["new"],
    "novo esboço":            geometry["new"],
    "criar esboço":           geometry["new"],

    "editar":                 geometry["edit"],
    "editar esboço":          geometry["edit"],

    "anexar":                 geometry["attach"],

    "grade":                  geometry["grid"],
    "grelha":                 geometry["grid"],

    "parar":                  geometry["stop"],

    "sair":                   geometry["leave"],
    "sair do esboço":         geometry["leave"],

    "ajuda":                  geometry["help"],
    "informação":             geometry["help"],
    "opções":                 geometry["help"],

    # MEASURE
    "medir": CreateDimension,
    "medida": CreateDimension,
    "medir distancia": CreateDimension,
    "medir distância": CreateDimension,
    "distância": CreateDimension,
    "distancia": CreateDimension,
    "cotar": CreateDimension,
    "dimensionar": CreateDimension,
    "aferir": CreateDimension,
    "mensurar": CreateDimension,
    "calcular distância": CreateDimension,
    "calcular distancia": CreateDimension,
    "comprimento": CreateDimension,
    "separação": CreateDimension,
    "separacao": CreateDimension,
    "afastamento": CreateDimension,
    "extensão": CreateDimension,
    "extensao": CreateDimension,
    "cota": CreateDimension,
    "cotagem": CreateDimension,
    "acotação": CreateDimension,
    "acotacao": CreateDimension,
    "dimensão": CreateDimension,
    "dimensao": CreateDimension,
    "métrica": CreateDimension,
    "metrica": CreateDimension,
    "dimensionamento": CreateDimension,
    "metro": CreateDimension,
    "milímetro": CreateDimension,
    "milimetro": CreateDimension,
    "centímetro": CreateDimension,
    "centimetro": CreateDimension,
    "flexômetro": CreateDimension,
    "flexometro": CreateDimension,
    "metro enrolável": CreateDimension,
    "metro enrolavel": CreateDimension,
    "régua": CreateDimension,
    "regua": CreateDimension,
    "escalímetro": CreateDimension,
    "escalimetro": CreateDimension,
    "calibre": CreateDimension,
    "paquímetro": CreateDimension,
    "paquimetro": CreateDimension,
    "micrômetro": CreateDimension,
    "micrometro": CreateDimension,
    "tolerância": CreateDimension,
    "tolerancia": CreateDimension,
    "desvio": CreateDimension,
    "ajuste": CreateDimension,
    "medição": CreateDimension,
    "medicao": CreateDimension,
    "mensuração": CreateDimension,
    "mensuracao": CreateDimension,
    "aferição": CreateDimension,
    "afericao": CreateDimension,
    "calibração": CreateDimension,
    "calibracao": CreateDimension,
    "verificação": CreateDimension,
    "verificacao": CreateDimension,
    "inspeção": CreateDimension,
    "inspecao": CreateDimension,
    "controle dimensional": CreateDimension,
    "metrologia": CreateDimension,
}

TraduceToPT = TraduceToPt
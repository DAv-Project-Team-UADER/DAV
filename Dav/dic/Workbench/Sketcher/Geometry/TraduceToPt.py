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
}

TraduceToPT = TraduceToPt

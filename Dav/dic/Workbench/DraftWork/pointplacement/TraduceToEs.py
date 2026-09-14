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

from .pointplacement import pointplacement

TraduceToEs = {
    "agregar punto":       pointplacement["addpoint"],
    "agregar_punto":       pointplacement["addpoint"],
    "poner punto":          pointplacement["addpoint"],
    "poner_punto":          pointplacement["addpoint"],
    
    "punto en vertice":    pointplacement["pointatvertex"],
    "punto en vértice":    pointplacement["pointatvertex"],
    "punto_en_vertice":    pointplacement["pointatvertex"],
    
    "punto medio":          pointplacement["midpoint"],
    "punto_medio":          pointplacement["midpoint"],
    "mitad":                pointplacement["midpoint"],
    
    "punto en coordenadas": pointplacement["pointatcoords"],
    "punto coordenadas":    pointplacement["pointatcoords"],
    "punto_en_coordenadas": pointplacement["pointatcoords"],
    
    "ayuda":                pointplacement["help"],
    "información":          pointplacement["help"],
    "opciones":             pointplacement["help"]
}

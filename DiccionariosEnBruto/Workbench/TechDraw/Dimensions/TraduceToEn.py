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

from .Dimensions import dimensions
from .ayuda import ayuda

TraduceToEn = {
    # vertical
    "vertical":           dimensions["vertical"],
    "vertical dimension": dimensions["vertical"],  # synonym
    "height":             dimensions["vertical"],  # synonym
    # area
    "area":               dimensions["area"],
    "area dimension":     dimensions["area"],      # synonym
    "surface":            dimensions["area"],      # synonym
    # fit
    "fit":                dimensions["fit"],
    "tolerance":          dimensions["fit"],       # synonym
    "hole shaft":         dimensions["fit"],       # synonym
    # length
    "length":             dimensions["length"],
    "distance":           dimensions["length"],    # synonym
    "measure":            dimensions["length"],    # synonym
    # horizontal
    "horizontal":         dimensions["horizontal"],
    "width":              dimensions["horizontal"], # synonym
    "x distance":         dimensions["horizontal"], # synonym
    # extent
    "extent":             dimensions["extent"],
    "span":               dimensions["extent"],    # synonym
    "total length":       dimensions["extent"],    # synonym
    # radius
    "radius":             dimensions["radius"],
    "arc radius":         dimensions["radius"],    # synonym
    # diameter
    "diameter":           dimensions["diameter"],
    "circle dimension":   dimensions["diameter"],  # synonym
    # angle
    "angle":              dimensions["angle"],
    "angular":            dimensions["angle"],     # synonym
    # help
    "help":               dimensions["help"],
    "info":               dimensions["help"],   # synonym
    "options":            dimensions["help"],   # synonym
}

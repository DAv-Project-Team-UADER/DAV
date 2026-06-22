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

"""English spoken-word mapping for the DAV joint dictionary."""
 
from .joint import joint
from .ayuda import ayuda
 
TraduceToEn = {
    "angle joint":         joint["angle"],
    "ball joint":          joint["ball"],
    "sphere joint":        joint["ball"],
    "parallel joint":      joint["parallel"],
    "perpendicular joint": joint["perpendicular"],
    "belt joint":          joint["belt"],
    "chain joint":         joint["belt"],
    "gear joint":          joint["gears"],
    "rack pinion":         joint["rackpinion"],
    "screw joint":         joint["screw"],
    "lead screw":          joint["screw"],
    "cylindrical joint":   joint["cylindrical"],
    "distance joint":      joint["distance"],
    "fixed joint":         joint["fixed"],
    "revolute joint":      joint["revolute"],
    "slider joint":        joint["slider"],

    "help":            joint["help"],
    "info":            joint["help"],
    "options":         joint["help"]

}
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

    # Angle
    "angle joint": joint["angle"],
    "angle": joint["angle"],

    # Ball
    "ball joint": joint["ball"],
    "ball": joint["ball"],
    "sphere joint": joint["ball"],
    "sphere": joint["ball"],

    # Parallel
    "parallel joint": joint["parallel"],
    "parallel": joint["parallel"],

    # Perpendicular
    "perpendicular joint": joint["perpendicular"],
    "perpendicular": joint["perpendicular"],

    # Belt
    "belt joint": joint["belt"],
    "belt": joint["belt"],
    "chain joint": joint["belt"],
    "chain": joint["belt"],

    # Gear
    "gear joint": joint["gears"],
    "gear": joint["gears"],
    "gears": joint["gears"],

    # Rack and pinion
    "rack pinion": joint["rackpinion"],
    "rack and pinion": joint["rackpinion"],
    "rack pinion joint": joint["rackpinion"],
    "rack and pinion joint": joint["rackpinion"],

    # Screw
    "screw joint": joint["screw"],
    "screw": joint["screw"],
    "lead screw": joint["screw"],

    # Cylindrical
    "cylindrical joint": joint["cylindrical"],
    "cylindrical": joint["cylindrical"],

    # Distance
    "distance joint": joint["distance"],
    "distance": joint["distance"],

    # Fixed
    "fixed joint": joint["fixed"],
    "fixed": joint["fixed"],

    # Revolute
    "revolute joint": joint["revolute"],
    "revolute": joint["revolute"],

    # Slider
    "slider joint": joint["slider"],
    "slider": joint["slider"],

    # Help
    "help": joint["help"],
    "info": joint["help"],
    "options": joint["help"]
}
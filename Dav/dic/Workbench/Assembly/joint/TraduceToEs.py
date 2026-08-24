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

"""Spanish spoken-word mapping for the DAV joint dictionary."""

from .joint import joint
from .ayuda import ayuda

TraduceToEs = {

    # Ángulo
    "union angular": joint["angle"],
    "unión angular": joint["angle"],
    "junta angular": joint["angle"],
    "union de angulo": joint["angle"],
    "unión de ángulo": joint["angle"],
    "restriccion de angulo": joint["angle"],
    "restricción de ángulo": joint["angle"],
    "angulo": joint["angle"],
    "ángulo": joint["angle"],

    # Rótula / Esférica
    "union esferica": joint["ball"],
    "unión esférica": joint["ball"],
    "junta esferica": joint["ball"],
    "junta esférica": joint["ball"],
    "union de esfera": joint["ball"],
    "unión de esfera": joint["ball"],
    "junta de esfera": joint["ball"],
    "rotula": joint["ball"],
    "rótula": joint["ball"],
    "union de rotula": joint["ball"],
    "unión de rótula": joint["ball"],
    "esferica": joint["ball"],
    "esférica": joint["ball"],

    # Paralela
    "union paralela": joint["parallel"],
    "unión paralela": joint["parallel"],
    "junta paralela": joint["parallel"],
    "union de paralelismo": joint["parallel"],
    "unión de paralelismo": joint["parallel"],
    "restriccion de paralelismo": joint["parallel"],
    "restricción de paralelismo": joint["parallel"],
    "paralela": joint["parallel"],
    "paralelo": joint["parallel"],
    "paralelismo": joint["parallel"],

    # Perpendicular
    "union perpendicular": joint["perpendicular"],
    "unión perpendicular": joint["perpendicular"],
    "junta perpendicular": joint["perpendicular"],
    "union de perpendicularidad": joint["perpendicular"],
    "unión de perpendicularidad": joint["perpendicular"],
    "restriccion de perpendicularidad": joint["perpendicular"],
    "restricción de perpendicularidad": joint["perpendicular"],
    "perpendicular": joint["perpendicular"],

    # Correa / Cadena
    "union de correa": joint["belt"],
    "unión de correa": joint["belt"],
    "junta de correa": joint["belt"],
    "union correa": joint["belt"],
    "unión correa": joint["belt"],
    "correa": joint["belt"],
    "union de cadena": joint["belt"],
    "unión de cadena": joint["belt"],
    "junta de cadena": joint["belt"],
    "union cadena": joint["belt"],
    "unión cadena": joint["belt"],
    "cadena": joint["belt"],

    # Engranajes
    "union de engranajes": joint["gears"],
    "unión de engranajes": joint["gears"],
    "union de engranaje": joint["gears"],
    "unión de engranaje": joint["gears"],
    "junta de engranajes": joint["gears"],
    "junta de engranaje": joint["gears"],
    "union engranajes": joint["gears"],
    "unión engranajes": joint["gears"],
    "engranajes": joint["gears"],
    "engranaje": joint["gears"],

    # Piñón-cremallera
    "union pinon cremallera": joint["rackpinion"],
    "unión piñón cremallera": joint["rackpinion"],
    "union piñon cremallera": joint["rackpinion"],
    "unión piñon cremallera": joint["rackpinion"],
    "union piñón cremallera": joint["rackpinion"],
    "junta piñón cremallera": joint["rackpinion"],
    "junta piñon cremallera": joint["rackpinion"],
    "union de piñon y cremallera": joint["rackpinion"],
    "unión de piñón y cremallera": joint["rackpinion"],
    "piñon cremallera": joint["rackpinion"],
    "piñón cremallera": joint["rackpinion"],
    "piñon y cremallera": joint["rackpinion"],
    "piñón y cremallera": joint["rackpinion"],
    "cremallera": joint["rackpinion"],

    # Helicoidal / Tornillo
    "union helicoidal": joint["screw"],
    "unión helicoidal": joint["screw"],
    "junta helicoidal": joint["screw"],
    "union de tornillo": joint["screw"],
    "unión de tornillo": joint["screw"],
    "junta de tornillo": joint["screw"],
    "tornillo": joint["screw"],
    "tornillo de avance": joint["screw"],
    "helicoidal": joint["screw"],

    # Cilíndrica
    "union cilindrica": joint["cylindrical"],
    "unión cilíndrica": joint["cylindrical"],
    "junta cilindrica": joint["cylindrical"],
    "junta cilíndrica": joint["cylindrical"],
    "union de cilindro": joint["cylindrical"],
    "unión de cilindro": joint["cylindrical"],
    "cilindrica": joint["cylindrical"],
    "cilíndrica": joint["cylindrical"],
    "cilindrico": joint["cylindrical"],
    "cilíndrico": joint["cylindrical"],

    # Distancia
    "union de distancia": joint["distance"],
    "unión de distancia": joint["distance"],
    "junta de distancia": joint["distance"],
    "restriccion de distancia": joint["distance"],
    "restricción de distancia": joint["distance"],
    "distancia": joint["distance"],

    # Fija
    "union fija": joint["fixed"],
    "unión fija": joint["fixed"],
    "junta fija": joint["fixed"],
    "union de fijacion": joint["fixed"],
    "unión de fijación": joint["fixed"],
    "junta de fijacion": joint["fixed"],
    "junta de fijación": joint["fixed"],
    "fijar": joint["fixed"],
    "fijo": joint["fixed"],
    "fija": joint["fixed"],

    # Revolución / Bisagra
    "union de revolucion": joint["revolute"],
    "unión de revolución": joint["revolute"],
    "junta de revolucion": joint["revolute"],
    "junta de revolución": joint["revolute"],
    "union revoluta": joint["revolute"],
    "unión revoluta": joint["revolute"],
    "junta revoluta": joint["revolute"],
    "revoluta": joint["revolute"],
    "revolucion": joint["revolute"],
    "revolución": joint["revolute"],
    "bisagra": joint["revolute"],

    # Deslizante / Prismática
    "union deslizante": joint["slider"],
    "unión deslizante": joint["slider"],
    "junta deslizante": joint["slider"],
    "union de deslizamiento": joint["slider"],
    "unión de deslizamiento": joint["slider"],
    "junta de deslizamiento": joint["slider"],
    "union prismatica": joint["slider"],
    "unión prismática": joint["slider"],
    "junta prismatica": joint["slider"],
    "junta prismática": joint["slider"],
    "deslizante": joint["slider"],
    "prismatica": joint["slider"],
    "prismática": joint["slider"],

    # Ayuda / Soporte
    "ayuda": joint["help"],
    "informacion": joint["help"],
    "información": joint["help"],
    "opciones": joint["help"]
}
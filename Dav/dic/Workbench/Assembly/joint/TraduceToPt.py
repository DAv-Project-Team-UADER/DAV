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

"""Mapeamento de palavras em portugues para o dicionario DAV joint."""
 
from .joint import joint
from .ayuda import ayuda
 
TraduceToPt = {
    "junta angular":       joint["angle"],
    "angulo":              joint["angle"],
    "junta esferica":      joint["ball"],
    "rotula":              joint["ball"],
    "junta paralela":      joint["parallel"],
    "paralelo":            joint["parallel"],
    "junta perpendicular": joint["perpendicular"],
    "perpendicular":       joint["perpendicular"],
    "junta correia":       joint["belt"],
    "correia":             joint["belt"],
    "junta engrenagem":    joint["gears"],
    "engrenagem":          joint["gears"],
    "cremalheira":         joint["rackpinion"],
    "pinhao cremalheira":  joint["rackpinion"],
    "junta parafuso":      joint["screw"],
    "fuso":                joint["screw"],
    "junta cilindrica":    joint["cylindrical"],
    "cilindrica":          joint["cylindrical"],
    "junta distancia":     joint["distance"],
    "distancia":           joint["distance"],
    "junta fixo":          joint["fixed"],
    "fixo":                joint["fixed"],
    "junta revoluta":      joint["revolute"],
    "revoluta":            joint["revolute"],
    "junta deslizante":    joint["slider"],
    "deslizante":          joint["slider"],
    
    "ajuda":               joint["help"],
    "informação":          joint["help"],
    "opções":              joint["help"]
}
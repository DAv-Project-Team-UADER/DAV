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

"""Mapeamento de palavras faladas em português para o dicionário DAV joint."""

from .joint import joint
from .ayuda import ayuda

TraduceToPt = {

    # Angular
    "união angular": joint["angle"],
    "uniao angular": joint["angle"],
    "junta angular": joint["angle"],
    "união de ângulo": joint["angle"],
    "uniao de angulo": joint["angle"],
    "junta de ângulo": joint["angle"],
    "junta de angulo": joint["angle"],
    "restrição de ângulo": joint["angle"],
    "restricao de angulo": joint["angle"],
    "ângulo": joint["angle"],
    "angulo": joint["angle"],

    # Esférica / Rótula
    "união esférica": joint["ball"],
    "uniao esferica": joint["ball"],
    "junta esférica": joint["ball"],
    "junta esferica": joint["ball"],
    "união de esfera": joint["ball"],
    "uniao de esfera": joint["ball"],
    "junta de esfera": joint["ball"],
    "rótula": joint["ball"],
    "rotula": joint["ball"],
    "união de rótula": joint["ball"],
    "uniao de rotula": joint["ball"],
    "esférica": joint["ball"],
    "esferica": joint["ball"],

    # Paralela
    "união paralela": joint["parallel"],
    "uniao paralela": joint["parallel"],
    "junta paralela": joint["parallel"],
    "união de paralelismo": joint["parallel"],
    "uniao de paralelismo": joint["parallel"],
    "junta de paralelismo": joint["parallel"],
    "restrição de paralelismo": joint["parallel"],
    "restricao de paralelismo": joint["parallel"],
    "paralela": joint["parallel"],
    "paralelo": joint["parallel"],
    "paralelismo": joint["parallel"],

    # Perpendicular
    "união perpendicular": joint["perpendicular"],
    "uniao perpendicular": joint["perpendicular"],
    "junta perpendicular": joint["perpendicular"],
    "união de perpendicularidade": joint["perpendicular"],
    "uniao de perpendicularidade": joint["perpendicular"],
    "junta de perpendicularidade": joint["perpendicular"],
    "restrição de perpendicularidade": joint["perpendicular"],
    "restricao de perpendicularidade": joint["perpendicular"],
    "perpendicular": joint["perpendicular"],

    # Correia / Corrente
    "união de correia": joint["belt"],
    "uniao de correia": joint["belt"],
    "junta de correia": joint["belt"],
    "união correia": joint["belt"],
    "uniao correia": joint["belt"],
    "junta correia": joint["belt"],
    "correia": joint["belt"],
    "união de corrente": joint["belt"],
    "uniao de corrente": joint["belt"],
    "junta de corrente": joint["belt"],
    "união corrente": joint["belt"],
    "uniao corrente": joint["belt"],
    "junta corrente": joint["belt"],
    "corrente": joint["belt"],

    # Engrenagens
    "união de engrenagens": joint["gears"],
    "uniao de engrenagens": joint["gears"],
    "união de engrenagem": joint["gears"],
    "uniao de engrenagem": joint["gears"],
    "junta de engrenagens": joint["gears"],
    "junta de engrenagem": joint["gears"],
    "união engrenagens": joint["gears"],
    "uniao engrenagens": joint["gears"],
    "junta engrenagens": joint["gears"],
    "união engrenagem": joint["gears"],
    "uniao engrenagem": joint["gears"],
    "junta engrenagem": joint["gears"],
    "engrenagens": joint["gears"],
    "engrenagem": joint["gears"],

    # Pinhão-cremalheira
    "união pinhão cremalheira": joint["rackpinion"],
    "uniao pinhao cremalheira": joint["rackpinion"],
    "junta pinhão cremalheira": joint["rackpinion"],
    "junta pinhao cremalheira": joint["rackpinion"],
    "união de pinhão e cremalheira": joint["rackpinion"],
    "uniao de pinhao e cremalheira": joint["rackpinion"],
    "junta de pinhão e cremalheira": joint["rackpinion"],
    "junta de pinhao e cremalheira": joint["rackpinion"],
    "pinhão cremalheira": joint["rackpinion"],
    "pinhao cremalheira": joint["rackpinion"],
    "pinhão e cremalheira": joint["rackpinion"],
    "pinhao e cremalheira": joint["rackpinion"],
    "cremalheira": joint["rackpinion"],

    # Helicoidal / Parafuso / Fuso
    "união helicoidal": joint["screw"],
    "uniao helicoidal": joint["screw"],
    "junta helicoidal": joint["screw"],
    "união de parafuso": joint["screw"],
    "uniao de parafuso": joint["screw"],
    "junta de parafuso": joint["screw"],
    "parafuso": joint["screw"],
    "fuso": joint["screw"],
    "fuso de avanço": joint["screw"],
    "fuso de avanco": joint["screw"],
    "parafuso de avanço": joint["screw"],
    "parafuso de avanco": joint["screw"],
    "helicoidal": joint["screw"],

    # Cilíndrica
    "união cilíndrica": joint["cylindrical"],
    "uniao cilindrica": joint["cylindrical"],
    "junta cilíndrica": joint["cylindrical"],
    "junta cilindrica": joint["cylindrical"],
    "união de cilindro": joint["cylindrical"],
    "uniao de cilindro": joint["cylindrical"],
    "junta de cilindro": joint["cylindrical"],
    "cilíndrica": joint["cylindrical"],
    "cilindrica": joint["cylindrical"],
    "cilíndrico": joint["cylindrical"],
    "cilindrico": joint["cylindrical"],

    # Distância
    "união de distância": joint["distance"],
    "uniao de distancia": joint["distance"],
    "junta de distância": joint["distance"],
    "junta de distancia": joint["distance"],
    "restrição de distância": joint["distance"],
    "restricao de distancia": joint["distance"],
    "distância": joint["distance"],
    "distancia": joint["distance"],

    # Fixa
    "união fixa": joint["fixed"],
    "uniao fixa": joint["fixed"],
    "junta fixa": joint["fixed"],
    "união de fixação": joint["fixed"],
    "uniao de fixacao": joint["fixed"],
    "junta de fixação": joint["fixed"],
    "junta de fixacao": joint["fixed"],
    "fixar": joint["fixed"],
    "fixo": joint["fixed"],
    "fixa": joint["fixed"],

    # Revolução / Dobradiça
    "união de revolução": joint["revolute"],
    "uniao de revolucao": joint["revolute"],
    "junta de revolução": joint["revolute"],
    "junta de revolucao": joint["revolute"],
    "união revoluta": joint["revolute"],
    "uniao revoluta": joint["revolute"],
    "junta revoluta": joint["revolute"],
    "revoluta": joint["revolute"],
    "revolução": joint["revolute"],
    "revolucao": joint["revolute"],
    "dobradiça": joint["revolute"],
    "dobradica": joint["revolute"],

    # Deslizante / Prismática
    "união deslizante": joint["slider"],
    "uniao deslizante": joint["slider"],
    "junta deslizante": joint["slider"],
    "união de deslizamento": joint["slider"],
    "uniao de deslizamento": joint["slider"],
    "junta de deslizamento": joint["slider"],
    "união prismática": joint["slider"],
    "uniao prismatica": joint["slider"],
    "junta prismática": joint["slider"],
    "junta prismatica": joint["slider"],
    "deslizante": joint["slider"],
    "prismática": joint["slider"],
    "prismatica": joint["slider"],

    # Ajuda / Suporte
    "ajuda": joint["help"],
    "informação": joint["help"],
    "informacao": joint["help"],
    "opções": joint["help"],
    "opcoes": joint["help"]
}
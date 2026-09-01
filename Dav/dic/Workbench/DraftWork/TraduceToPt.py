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

TraduceToPt = {
    'anotacao':   draft['annotation'],
    'anotação':   draft['annotation'],
    'nota':       draft['annotation'],
    'texto':      draft['annotation'],
    'escrever':    draft['annotation'],
    

    'arco':       draft['arc'],

    'curva':      draft['curve'],
    'spline':     draft['curve'],

    'circulo':    draft['circle'],
    'círculo':    draft['circle'],

    'matriz':     draft['array'],
    'padrao':     draft['array'],
    'padrão':     draft['array'],
    'matriz circular': draft['array'],

    'modificar':  draft['modify'],
    'editar':     draft['modify'],
    'mudar':      draft['modify'],

    'dimensao':   draft['dimension'],
    'dimensão':   draft['dimension'],
    'medida':     draft['dimension'],
    'medir':      draft['dimension'],

    'elipse':     draft['ellipse'],
    'ovalo':      draft['ellipse'],
    'óvalo':      draft['ellipse'],

    'facebinder': draft['facebinder'],
    'binder':     draft['facebinder'],
    'aglutinante': draft['facebinder'],

    'colocacao de pontos': draft['pointplacement'],
    'colocação de pontos': draft['pointplacement'],
    'posicionar ponto':    draft['pointplacement'],

    'conectar pontos': draft['pointconnect'],
    'conexao de pontos': draft['pointconnect'],
    'conexão de pontos': draft['pointconnect'],

    "ajuda":             draft["help"],
    "informação":       draft["help"],
    "opções":            draft["help"]
,
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
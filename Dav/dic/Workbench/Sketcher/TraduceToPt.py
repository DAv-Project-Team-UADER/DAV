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

from .sketcher import sketcher as Sketcher
import FreeCADGui as Gui

# Importaciones relativas porque estamos en la misma carpeta
from .sketcher import _toggle_construction
from .ayuda import ayuda as sketcher_ayuda
from .sketcher import sketcher
from measure import CreateDimension

TraduceToPt = {
  
  # Carpetas de Sketcher  
  "geometria": sketcher["geometry"],

  "arco": sketcher["arcslot"],
  "arcos": sketcher["arcslot"],
  "ranhura de arco": sketcher["arcslot"],

  "restricoes": sketcher["constraints"],
  "restrições": sketcher["constraints"],
  "restricao": sketcher["constraints"],
  "restrição": sketcher["constraints"],

  "externo": sketcher["external"],
  "externa": sketcher["external"],

  "oblongo": sketcher["oblong"],
  "criar oblongo": sketcher["oblong"],

  "ponto": sketcher["point"],
  "criar ponto": sketcher["point"],

  "selecionar": sketcher["select"],
  "selecao": sketcher["select"],
  "seleção": sketcher["select"],

  "ranhura": sketcher["slot"],
  "criar ranhura": sketcher["slot"],

  "quadrado": sketcher["square"],
  "criar quadrado": sketcher["square"],
  "desenhar quadrado": sketcher["square"],

  "texto": sketcher["text"],
  "escrever texto": sketcher["text"],
  "criar texto": sketcher["text"],

  "ferramentas": sketcher["tools"],
  "ferramenta": sketcher["tools"],

  "triangulo": sketcher["triangle"],
  "triângulo": sketcher["triangle"],
  "criar triangulo": sketcher["triangle"],
  "criar triângulo": sketcher["triangle"],
  "desenhar triangulo": sketcher["triangle"],
  "desenhar triângulo": sketcher["triangle"],

  "validar": sketcher["validate"],
  "validar esboco": sketcher["validate"],
  "validar esboço": sketcher["validate"],

  "vista": sketcher["view"],
  "ver esboco": sketcher["view"],
  "ver esboço": sketcher["view"],
  "ver selecao": sketcher["view"],
  "ver seleção": sketcher["view"],

  # Controle do Esboço / Sketch
   "novo": sketcher["new"],
   "novo esboço": sketcher["new"],
   "criar esboço": sketcher["new"],

   "editar": sketcher["edit"],
   "editar esboço": sketcher["edit"],
   "modificar esboço": sketcher["edit"],

   "anexar": sketcher["attach"],
   "mapear esboço": sketcher["attach"],
   "anexar esboço": sketcher["attach"],

   "grade": sketcher["grid"],
   "alternar grade": sketcher["grid"],
   "mostrar grade": sketcher["grid"],

   "parar": sketcher["stop"],
   "parar operação": sketcher["stop"],
   "abortar": sketcher["stop"],

   "sair": sketcher["leave"],
   "sair do esboço": sketcher["leave"],
   "sair esboço": sketcher["leave"],
   "fechar esboço": sketcher["leave"],

   "cancelaredit": sketcher["cancelediting"],
   "cancelar edição": sketcher["cancelediting"],
   "parar edição": sketcher["cancelediting"],

   # Geometria de Construção
   "alternar construção": _toggle_construction,
   "modo construção": _toggle_construction,
   "alternar geometria de construção": _toggle_construction,

   # Edição e Área de Transferência
   "duplicar": sketcher["carboncopy"],
   "cópia carbono": sketcher["carboncopy"],

   "copiar elementos": sketcher["copyelements"],
   "copiar geometria": sketcher["copyelements"],
   "copiar": sketcher["copyelements"],

   "recortar elementos": sketcher["cutelements"],
   "recortar geometria": sketcher["cutelements"],
   "recortar": sketcher["cutelements"],

   "colar elementos": sketcher["pasteelements"],
   "colar geometria": sketcher["pasteelements"],
   "colar": sketcher["pasteelements"],

   # Transformações e Modificações
   "simetria": sketcher["mirror"],
   "espelho": sketcher["mirror"],
   "refletir elementos": sketcher["mirror"],

   "espelhar esboço": sketcher["mirrorsketch"],
   "refletir esboço": sketcher["mirrorsketch"],

   "deslocamento": sketcher["offset"],
   "criar deslocamento": sketcher["offset"],

   "mover": sketcher["movearray"],
   "mover elementos": sketcher["movearray"],
   "transladar": sketcher["movearray"],

   "rodar": sketcher["rotatepolar"],
   "rodar elementos": sketcher["rotatepolar"],
   "rotação polar": sketcher["rotatepolar"],

   "escalar": sketcher["scale"],
   "escalar elementos": sketcher["scale"],

   # Operações de Arestas / Cantos
   "recortar": sketcher["trimedge"],
   "recortar aresta": sketcher["trimedge"],
   "recortar borda": sketcher["trimedge"],

   "dividir aresta": sketcher["splitedge"],
   "dividir": sketcher["splitedge"],
   "separar aresta": sketcher["splitedge"],

   "estender aresta": sketcher["extendedge"],
   "estender": sketcher["extendedge"],
   "estender borda": sketcher["extendedge"],

   "filete": sketcher["fillet"],
   "criar filete": sketcher["fillet"],
   "arredondar": sketcher["fillet"],

   "chanfro": sketcher["chamfer"],
   "criar chanfro": sketcher["chamfer"],
   "chanfrear": sketcher["chamfer"],


  "ajuda": Sketcher['help'],
  "informação": Sketcher['help'],
  "opções": Sketcher['help'],

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
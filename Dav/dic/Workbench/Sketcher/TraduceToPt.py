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

import FreeCADGui as Gui

# Importaciones relativas porque estamos en la misma carpeta
from .Sketcher import _toggle_construction
from .ayuda import ayuda as sketcher_ayuda
from .Sketcher import sketcher

TranslateToPt = {
  
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
}

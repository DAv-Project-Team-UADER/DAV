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

TraduceToEs = {
  "geometria": sketcher["geometry"],
  "geometría": sketcher["geometry"],

  "arco": sketcher["arcslot"],
  "arcos": sketcher["arcslot"],
  "ranura de arco": sketcher["arcslot"],

  "restricciones": sketcher["constraints"],
  "restriccion": sketcher["constraints"],
  "restricción": sketcher["constraints"],

  "externo": sketcher["external"],
  "externa": sketcher["external"],

  "oblongo": sketcher["oblong"],
  "crear oblongo": sketcher["oblong"],

  "punto": sketcher["point"],
  "crear punto": sketcher["point"],

  "seleccionar": sketcher["select"],
  "seleccion": sketcher["select"],
  "selección": sketcher["select"],

  "ranura": sketcher["slot"],
  "crear ranura": sketcher["slot"],

  "cuadrado": sketcher["square"],
  "crear cuadrado": sketcher["square"],
  "dibujar cuadrado": sketcher["square"],

  "texto": sketcher["text"],
  "escribir texto": sketcher["text"],
  "crear texto": sketcher["text"],

  "herramientas": sketcher["tools"],
  "herramienta": sketcher["tools"],

  "triangulo": sketcher["triangle"],
  "triángulo": sketcher["triangle"],
  "crear triangulo": sketcher["triangle"],
  "crear triángulo": sketcher["triangle"],
  "dibujar triangulo": sketcher["triangle"],
  "dibujar triángulo": sketcher["triangle"],

  "validar": sketcher["validate"],
  "validar croquis": sketcher["validate"],

  "vista": sketcher["view"],
  "ver croquis": sketcher["view"],
  "ver seleccion": sketcher["view"],
  "ver selección": sketcher["view"],
}

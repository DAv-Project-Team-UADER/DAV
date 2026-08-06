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
from .sketcher import _toggle_construction
from .ayuda import ayuda as sketcher_ayuda
from .sketcher import sketcher

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

  # Control del Boceto / Sketch
   "nuevo": sketcher["new"],
   "nuevo croquis": sketcher["new"],
   "crear croquis": sketcher["new"],

   "editar": sketcher["edit"],
   "editar croquis": sketcher["edit"],
   "modificar croquis": sketcher["edit"],

   "adjuntar": sketcher["attach"],
   "mapear croquis": sketcher["attach"],
   "adjuntar croquis": sketcher["attach"],

   "cuadrícula": sketcher["grid"],
   "alternar cuadrícula": sketcher["grid"],
   "mostrar cuadrícula": sketcher["grid"],

   "detener": sketcher["stop"],
   "detener operación": sketcher["stop"],
   "abortar": sketcher["stop"],

   "salir": sketcher["leave"],
   "salir del croquis": sketcher["leave"],
   "salir croquis": sketcher["leave"],
   "cerrar croquis": sketcher["leave"],

   "cancelaredit": sketcher["cancelediting"],
   "cancelar edición": sketcher["cancelediting"],
   "detener edición": sketcher["cancelediting"],

   # Geometría de Construcción
   "alternar construcción": _toggle_construction,
   "modo construcción": _toggle_construction,
   "alternar geometría de construcción": _toggle_construction,

   # Edición y Portapapeles
   "duplicar": sketcher["carboncopy"],
   "copia carbono": sketcher["carboncopy"],

   "copiar elementos": sketcher["copyelements"],
   "copiar geometría": sketcher["copyelements"],
   "copiar": sketcher["copyelements"],

   "cortar elementos": sketcher["cutelements"],
   "cortar geometría": sketcher["cutelements"],
   "cortar": sketcher["cutelements"],

   "pegar elementos": sketcher["pasteelements"],
   "pegar geometría": sketcher["pasteelements"],
   "pegar": sketcher["pasteelements"],

   # Transformaciones y Modificaciones
   "simetría": sketcher["mirror"],
   "espejo": sketcher["mirror"],
   "reflejar elementos": sketcher["mirror"],

   "espejar croquis": sketcher["mirrorsketch"],
   "reflejar croquis": sketcher["mirrorsketch"],

   "desplazamiento": sketcher["offset"],
   "crear desplazamiento": sketcher["offset"],

   "mover": sketcher["movearray"],
   "mover elementos": sketcher["movearray"],
   "trasladar": sketcher["movearray"],

   "rotar": sketcher["rotatepolar"],
   "rotar elementos": sketcher["rotatepolar"],
   "rotación polar": sketcher["rotatepolar"],

   "escalar": sketcher["scale"],
   "escalar elementos": sketcher["scale"],

   # Operaciones de Bordes / Esquinas
   "recortar": sketcher["trimedge"],
   "recortar arista": sketcher["trimedge"],
   "recortar borde": sketcher["trimedge"],

   "dividir arista": sketcher["splitedge"],
   "dividir": sketcher["splitedge"],
   "separar arista": sketcher["splitedge"],

   "extender arista": sketcher["extendedge"],
   "extender": sketcher["extendedge"],
   "extender borde": sketcher["extendedge"],

   "filete": sketcher["fillet"],
   "crear filete": sketcher["fillet"],
   "redondear": sketcher["fillet"],

   "chaflán": sketcher["chamfer"],
   "crear chaflán": sketcher["chamfer"],
   "chanflear": sketcher["chamfer"],


  "ayuda": sketcher['help'],
  "información": sketcher['help'],
  "opciones": sketcher['help'],
}

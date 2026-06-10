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
from .Geometry.geometry import geometry
from .arcslot.arcslot import arcslot
from .constraints.constraints import constraints
from .external.external import external
from .oblong.oblong import oblong
from .point.point import point
from .select.select import select
from .slot.slot import slot
from .square.square import square
from .text.text import text
from .tools.tools import tools
from .triangle.triangle import triangle
from .validate.validate import validate
from .view.view import view

TraduceToEs = {
  "geometria": "geometry",
  "geometría": "geometry",

  "arco": "arc",
  "arcos": "arcs",
  "ranura de arco": "arcslot",

  "restricciones": "constraints",
  "restriccion": "constraint",
  "restricción": "constraint",

  "externo": "external",
  "externa": "external",

  "oblongo": "oblong",
  "crear oblongo": "create oblong",

  "punto": "point",
  "crear punto": "create point",

  "seleccionar": "select",
  "seleccion": "selection",
  "selección": "selection",

  "ranura": "slot",
  "crear ranura": "create slot",

  "cuadrado": "square",
  "crear cuadrado": "create square",
  "dibujar cuadrado": "draw square",

  "texto": "text",
  "escribir texto": "write text",
  "crear texto": "create text",

  "herramientas": "tools",
  "herramienta": "tool",

  "triangulo": "triangle",
  "triángulo": "triangle",
  "crear triangulo": "create triangle",
  "crear triángulo": "create triangle",
  "dibujar triangulo": "draw triangle",
  "dibujar triángulo": "draw triangle",

  "validar": "validate",
  "validar croquis": "validate sketch",

  "vista": "view",
  "ver croquis": "view sketch",
  "ver seleccion": "view selection",
  "ver selección": "view selection",
}

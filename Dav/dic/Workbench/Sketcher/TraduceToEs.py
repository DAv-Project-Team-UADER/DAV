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
from measure import CreateDimension

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
   "nuevo boceto": sketcher["new"],
   "crear boceto": sketcher["new"],
   "boceto nuevo": sketcher["new"],

   "editar": sketcher["edit"],
   "editar croquis": sketcher["edit"],
   "modificar croquis": sketcher["edit"],

   "adjuntar": sketcher["attach"],
   "mapear croquis": sketcher["attach"],
   "adjuntar croquis": sketcher["attach"],

    "cuadrícula": sketcher["grid"],
    "alternar cuadrícula": sketcher["grid"],
    "mostrar cuadrícula": sketcher["grid"],

    "cerrar croquis": sketcher["leave"],
    "cerrar boceto": sketcher["leave"],
    "salir del croquis": sketcher["leave"],
    "salir del boceto": sketcher["leave"],
    "terminar croquis": sketcher["leave"],
    "terminar boceto": sketcher["leave"],
    "finalizar croquis": sketcher["leave"],

    "cancelar edición": sketcher["cancelediting"],
   "detener edición": sketcher["cancelediting"],
   "cancelar": sketcher["cancelediting"],

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
   "chaflanar": sketcher["chamfer"],
   "biselar": sketcher["chamfer"],


  "ayuda": sketcher['help'],
  "información": sketcher['help'],
  "opciones": sketcher['help'],

    # MEASURE
    "medir": CreateDimension,
    "medir distancia": CreateDimension,
    "acotar": CreateDimension,
    "dimensionar": CreateDimension,
    "cotar": CreateDimension,
    "distancia": CreateDimension,
    "medida": CreateDimension,
    "longitud": CreateDimension,
    "separación": CreateDimension,
    "separacion": CreateDimension,
    "cota": CreateDimension,
    "acotación": CreateDimension,
    "acotacion": CreateDimension,
    "dimensión": CreateDimension,
    "dimension": CreateDimension,
    "métrica": CreateDimension,
    "metrica": CreateDimension,
    "metro": CreateDimension,
    "milímetro": CreateDimension,
    "milimetro": CreateDimension,
    "centímetro": CreateDimension,
    "centimetro": CreateDimension,
    "cinta": CreateDimension,
    "flexómetro": CreateDimension,
    "flexometro": CreateDimension,
    "metro enrollable": CreateDimension,
    "regla": CreateDimension,
    "escalímetro": CreateDimension,
    "escalimetro": CreateDimension,
    "calibre": CreateDimension,
    "pie de rey": CreateDimension,
    "línea de cota": CreateDimension,
    "linea de cota": CreateDimension,
    "cota lineal": CreateDimension,
    "acotación lineal": CreateDimension,
    "acotacion lineal": CreateDimension,
    "dimensionado": CreateDimension,
    "micrómetro": CreateDimension,
    "micrometro": CreateDimension,
}

from dic.StdView.StandardViews.StandardViews import *

TraduceToEs.update ({
    # bottom
    'abajo':                StandardViews['bottom'],
    'inferior':             StandardViews['bottom'],
    'vista abajo':          StandardViews['bottom'],
    'vista inferior':       StandardViews['bottom'],
    'desde abajo':          StandardViews['bottom'],
    'vista baja':          StandardViews['bottom'],

    # boxzoom
    'zoom caja':            StandardViews['boxzoom'],
    'zoom rectangular':     StandardViews['boxzoom'],
    'zoom area':            StandardViews['boxzoom'],
    'zoom por caja':        StandardViews['boxzoom'],
    'zoom de area':         StandardViews['boxzoom'],

    # newview
    'nueva vista':          StandardViews['newview'],
    'crear vista':          StandardViews['newview'],
    'ventana nueva':        StandardViews['newview'],
    'nueva ventana':        StandardViews['newview'],

    # dimetric
    'dimetrica':            StandardViews['dimetric'],
    'dimétrica':            StandardViews['dimetric'],
    'vista dimetrica':      StandardViews['dimetric'],
    'vista dimétrica':      StandardViews['dimetric'],

    # fitall
    'ajustar todo':         StandardViews['fitall'],
    'encuadrar todo':       StandardViews['fitall'],
    'ver todo':             StandardViews['fitall'],
    'zoom todo':            StandardViews['fitall'],
    'ajustar a todo':       StandardViews['fitall'],

    # fitselection
    'ajustar seleccion':    StandardViews['fitselection'],
    'ajustar selección':    StandardViews['fitselection'],
    'encuadrar seleccion':  StandardViews['fitselection'],
    'encuadrar selección':  StandardViews['fitselection'],
    'zoom seleccion':       StandardViews['fitselection'],
    'zoom selección':       StandardViews['fitselection'],

    # front
    'frontal':              StandardViews['front'],
    'frente':               StandardViews['front'],
    'vista frontal':        StandardViews['front'],
    'desde el frente':      StandardViews['front'],
    'vista de frente':      StandardViews['front'],

    # fullscreen
    'pantalla completa':    StandardViews['fullscreen'],
    'pantalla entera':      StandardViews['fullscreen'],
    'maximizar vista':      StandardViews['fullscreen'],
    'modo pantalla completa': StandardViews['fullscreen'],

    # home
    'inicio':               StandardViews['home'],
    'vista inicial':        StandardViews['home'],
    'vista predeterminada': StandardViews['home'],
    'restablecer vista':    StandardViews['home'],
    'vista por defecto':    StandardViews['home'],

    # isometric
    'isometrica':           StandardViews['isometric'],
    'isométrica':           StandardViews['isometric'],
    'vista isometrica':     StandardViews['isometric'],
    'vista isométrica':     StandardViews['isometric'],
    'tres de':              StandardViews['isometric'],
    'profundidad':          StandardViews['isometric'],
    'vista de tres de':      StandardViews['isometric'],
    'vista de profundidad':  StandardViews['isometric'],
    'proyectar':             StandardViews['isometric'],

    # left
    'izquierda':            StandardViews['left'],
    'izquierdo':            StandardViews['left'],
    'vista izquierda':      StandardViews['left'],
    'lateral izquierdo':    StandardViews['left'],
    'desde la izquierda':   StandardViews['left'],
    'vista de izquierda':    StandardViews['left'],
    'lado' :                  StandardViews['left'],

    # rear
    'trasera':              StandardViews['rear'],
    'detras':               StandardViews['rear'],
    'atrás':                StandardViews['rear'],
    'vista trasera':        StandardViews['rear'],
    'posterior':            StandardViews['rear'],
    'desde atras':          StandardViews['rear'],

    # right
    'derecha':              StandardViews['right'],
    'derecho':              StandardViews['right'],
    'vista derecha':        StandardViews['right'],
    'lateral derecho':      StandardViews['right'],
    'desde la derecha':     StandardViews['right'],

    # top
    'arriba':               StandardViews['top'],
    'superior':             StandardViews['top'],
    'vista superior':       StandardViews['top'],
    'planta':               StandardViews['top'],
    'desde arriba':         StandardViews['top'],
    'vista de arriba':      StandardViews['top'],

    # trimetric
    'trimetrica':           StandardViews['trimetric'],
    'trimétrica':           StandardViews['trimetric'],
    'vista trimetrica':     StandardViews['trimetric'],
    'vista trimétrica':     StandardViews['trimetric'],

    # zoomin
    'acercar':              StandardViews['zoomin'],
    'zoom acercar':         StandardViews['zoomin'],
    'aumentar zoom':        StandardViews['zoomin'],
    'zoom mas':             StandardViews['zoomin'],
    'zoom más':             StandardViews['zoomin'],

    # zoomout
    'alejar':               StandardViews['zoomout'],
    'zoom alejar':          StandardViews['zoomout'],
    'disminuir zoom':       StandardViews['zoomout'],
    'zoom menos':           StandardViews['zoomout'],

})

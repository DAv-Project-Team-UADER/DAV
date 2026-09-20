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

"""Spanish spoken-word mapping for the Sketcher tools dictionary."""

from .tools import tools
from .ayuda import ayuda
from measure import CreateDimension

TraduceToEs = {
    
    # Borrar restricciones y sinónimos
    "borrar restricciones": tools['deleteconstraints'],
    "limpiar restricciones": tools['deleteconstraints'],
    "eliminar restricciones": tools['deleteconstraints'],
    
    # Borrar geometría y sinónimos
    "borrar geometria": tools['deletegeometry'],
    "limpiar geometria": tools['deletegeometry'],
    "borrar croquis": tools['deletegeometry'],
    # "cerrar croquis" se parece a "borrar croquis": se registra acá para que
    # la coincidencia exacta gane y nunca se confunda con borrar todo
    "cerrar croquis": tools['leave'],
    "cerrar boceto": tools['leave'],
    "salir del croquis": tools['leave'],
    "salir del boceto": tools['leave'],
    "terminar croquis": tools['leave'],
    "terminar boceto": tools['leave'],
    "finalizar croquis": tools['leave'],
    "limpiar croquis": tools['deletegeometry'],
    
    # Fusionar y sinónimos
    "fusionar": tools['merge'],
    "fusionar croquis": tools['merge'],
    "combinar croquis": tools['merge'],
    
    # Reorientar y sinónimos
    "reorientar": tools['reorient'],
    "reorientar croquis": tools['reorient'],
    "cambiar plano del croquis": tools['reorient'],
    
    # Remover alineación de ejes y sinónimos
    "remover ejes": tools['removeaxes'],
    "quitar alineacion de ejes": tools['removeaxes'],

    "ayuda": tools['help'],
    "información": tools['help'],
    "opciones": tools['help']
,
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

# Mover la vista (centra la cámara en un punto)
from moveview import MoveView, MOVE_VIEW_PHRASES
for _phrase in MOVE_VIEW_PHRASES['es']:
    TraduceToEs.setdefault(_phrase, MoveView)

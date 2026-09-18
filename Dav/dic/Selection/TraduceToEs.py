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

from .selection import selection
from .ayuda import ayuda

TraduceToEs = {
    # next
    "avanzar": selection["next"],
    "otro": selection["next"],
    "otra": selection["next"],
    "pasar": selection["next"],
    "siguiente": selection["next"],
    "siguiente objeto": selection["next"],
    "objeto siguiente": selection["next"],
    "siguiente elemento": selection["next"],
    "seleccionar siguiente": selection["next"],
    "seleccionar siguiente objeto": selection["next"],

    # previous
    "retroceder": selection["previous"],
    "volver": selection["previous"],
    "anterior": selection["previous"],
    "anterior objeto": selection["previous"],
    "objeto anterior": selection["previous"],
    "anterior elemento": selection["previous"],
    "seleccionar anterior": selection["previous"],
    "seleccionar anterior objeto": selection["previous"],

    # selectall
    "todos": selection["selectall"],
    "todo": selection["selectall"],
    "seleccionar todos": selection["selectall"],
    "seleccionar todo": selection["selectall"],
    "seleccionar todos los objetos": selection["selectall"],

    # deselectall
    "nada": selection["deselectall"],
    "ninguno": selection["deselectall"],
    "ninguna": selection["deselectall"],
    "quitar": selection["deselectall"],
    "quitar todos": selection["deselectall"],
    "desmarcar": selection["deselectall"],
    "desmarcar todo": selection["deselectall"],
    "desmarcar todos": selection["deselectall"],
    "deseleccionar": selection["deselectall"],
    "deseleccionar todo": selection["deselectall"],
    "deseleccionar todos": selection["deselectall"],
    "limpiar seleccion": selection["deselectall"],
    "limpiar seleccion": selection["deselectall"],

    # current
    "cual": selection["current"],
    "este": selection["current"],
    "actual": selection["current"],
    "objeto actual": selection["current"],
    "que objeto tengo": selection["current"],

    # count
    "cuantos": selection["count"],
    "cantidad": selection["count"],
    "cuantos objetos": selection["count"],
    "cuantos hay": selection["count"],

    # delete — borrar el objeto actualmente seleccionado (avanzar/anterior + borrar)
    "borrar": selection["delete"],
    "borrar objeto": selection["delete"],
    "borrar elemento": selection["delete"],
    "borrar seleccion": selection["delete"],
    "borrar selección": selection["delete"],
    "eliminar": selection["delete"],
    "eliminar objeto": selection["delete"],
    "eliminar elemento": selection["delete"],
    "eliminar seleccion": selection["delete"],
    "eliminar selección": selection["delete"],
    "suprimir": selection["delete"],
    "suprimir objeto": selection["delete"],
    "quitar objeto": selection["delete"],

    "ayuda": ayuda,
    "help": ayuda,
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

    # left
    'izquierda':            StandardViews['left'],
    'izquierdo':            StandardViews['left'],
    'vista izquierda':      StandardViews['left'],
    'lateral izquierdo':    StandardViews['left'],
    'desde la izquierda':   StandardViews['left'],

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

    # help
    'ayuda':                StandardViews['help'],
    "información":          StandardViews['help'],
    'opciones':             StandardViews['help'],
})
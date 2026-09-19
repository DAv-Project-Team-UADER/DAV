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

"""Spanish spoken-word mapping for the DAV StdView/Visibility dictionary folder."""

from .Visibility import visibility

TraduceToEs = {
    "volver atrás":         visibility["selback"],

    "ocultar objetos":      visibility["hideobjects"],
    "ocultar todo":         visibility["hideobjects"],
    "ocultar todos":        visibility["hideobjects"],
    "esconder objetos":     visibility["hideobjects"],
    "esconder todo":        visibility["hideobjects"],

    "ocultar":              visibility["hide"],
    "esconder":             visibility["hide"],
    "ocultar seleccion":    visibility["hide"],
    "ocultar selección":    visibility["hide"],
    "esconder seleccion":   visibility["hide"],
    "esconder selección":   visibility["hide"],

    "todos los links":      visibility["alllinks"],
    "todos los enlaces":    visibility["alllinks"],
    "seleccionar todos los links": visibility["alllinks"],
    "seleccionar todos los enlaces": visibility["alllinks"],

    "vinculado":            visibility["linked"],
    "objeto vinculado":     visibility["linked"],
    "enlazado":             visibility["linked"],
    "ir al vinculo":        visibility["linked"],
    "ir al vínculo":        visibility["linked"],

    "vinculo final":        visibility["linkedfinal"],
    "vínculo final":        visibility["linkedfinal"],
    "enlace final":         visibility["linkedfinal"],
    "vinculado final":      visibility["linkedfinal"],

    "atras seleccion":      visibility["selback"],
    "atrás selección":      visibility["selback"],
    "retroceder seleccion":  visibility["selback"],
    "retroceder selección":  visibility["selback"],
    "volver seleccion":     visibility["selback"],
    "volver selección":     visibility["selback"],

    "caja de colision":     visibility["boundingbox"],
    "caja de colisión":     visibility["boundingbox"],
    "caja delimitadora":    visibility["boundingbox"],
    "caja limite":          visibility["boundingbox"],
    "caja límite":          visibility["boundingbox"],
    "caja de límites":      visibility["boundingbox"],

    "adelante seleccion":   visibility["selforward"],
    "adelante selección":   visibility["selforward"],
    "avanzar seleccion":    visibility["selforward"],
    "avanzar selección":    visibility["selforward"],

    "seleccionar visibles": visibility["selectvisible"],
    "seleccionar visible":  visibility["selectvisible"],
    "seleccionar objetos visibles": visibility["selectvisible"],

    "mostrar objetos":      visibility["showobjects"],
    "mostrar todo":         visibility["showobjects"],
    "mostrar todos":        visibility["showobjects"],
    "hacer visible todo":   visibility["showobjects"],
    "revelar objetos":      visibility["showobjects"],

    "mostrar":              visibility["show"],
    "revelar":              visibility["show"],
    "mostrar seleccion":    visibility["show"],
    "mostrar selección":    visibility["show"],

    "alternar todo":        visibility["toggleall"],
    "conmutar todo":        visibility["toggleall"],
    "alternar todos":       visibility["toggleall"],

    "seleccionabilidad":    visibility["selectability"],
    "alternar seleccionabilidad": visibility["selectability"],
    "alternar selecciónabilidad": visibility["selectability"],
    "permitir seleccion":   visibility["selectability"],
    "permitir selección":   visibility["selectability"],

    "transparencia":        visibility["transparency"],
    "alternar transparencia": visibility["transparency"],
    "transparente":         visibility["transparency"],

    "alternar":             visibility["toggle"],
    "alternar visibilidad": visibility["toggle"],
    "conmutar visibilidad": visibility["toggle"],

    "alinear a seleccion":  visibility["aligntoselection"],
    "alinear a selección":  visibility["aligntoselection"],
    "alinear con seleccion": visibility["aligntoselection"],
    "alinear con selección": visibility["aligntoselection"],
    "perpendicular a la seleccion": visibility["aligntoselection"],
    "perpendicular a la selección": visibility["aligntoselection"],

    "ayuda":                visibility["help"],
    "información":          visibility["help"],
    "opciones":             visibility["help"],
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
    # Vosk suele oír solo "metrica" (medir). Preferir "iso".
    'iso':                  StandardViews['isometric'],
    'vista iso':            StandardViews['isometric'],
    'iso metrica':          StandardViews['isometric'],
    'iso métrica':          StandardViews['isometric'],
    'iso isometrica':       StandardViews['isometric'],
    'iso isométrica':       StandardViews['isometric'],
    'isometrica':           StandardViews['isometric'],
    'isométrica':           StandardViews['isometric'],
    'vista isometrica':     StandardViews['isometric'],
    'vista isométrica':     StandardViews['isometric'],
    'axonometrica':         StandardViews['isometric'],
    'axonométrica':         StandardViews['isometric'],
    'vista axonometrica':   StandardViews['isometric'],
    'vista axonométrica':   StandardViews['isometric'],

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

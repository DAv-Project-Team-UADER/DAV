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

"""Spanish spoken-word mapping for TechDraw workbench dictionary."""

from .TechDraw import techdraw

TraduceToEs = {
    # Submenús de TechDraw
    "vistas":                 techdraw["views"],
    "vista":                  techdraw["views"],
    "vistas principales":     techdraw["views"],

    "dimensiones":            techdraw["dimensions"],
    "dimension":              techdraw["dimensions"],
    "dimensión":              techdraw["dimensions"],
    "cotas":                  techdraw["dimensions"],
    "cota":                   techdraw["dimensions"],
    "acotaciones":            techdraw["dimensions"],
    "acotacion":              techdraw["dimensions"],
    "acotación":              techdraw["dimensions"],
    "medidas":                techdraw["dimensions"],

    "lineas":                 techdraw["addlines"],
    "líneas":                 techdraw["addlines"],
    "linea":                  techdraw["addlines"],
    "línea":                  techdraw["addlines"],
    "agregar lineas":         techdraw["addlines"],
    "agregar líneas":         techdraw["addlines"],

    "simbolos":               techdraw["symbols"],
    "símbolos":               techdraw["symbols"],
    "simbolo":                techdraw["symbols"],
    "símbolo":                techdraw["symbols"],

    "capturas":               techdraw["snaps"],
    "enganches":              techdraw["snaps"],
    "snaps":                  techdraw["snaps"],
    "puntos de ajuste":       techdraw["snaps"],

    "topologia":              techdraw["topology"],
    "topología":              techdraw["topology"],
    "elementos topológicos":  techdraw["topology"],

    "pagina":                 techdraw["page"],
    "página":                 techdraw["page"],
    "hoja":                   techdraw["page"],
    "hoja de dibujo":         techdraw["page"],
    "plantilla":              techdraw["page"],

    "anotaciones":            techdraw["annotations"],
    "anotacion":              techdraw["annotations"],
    "anotación":              techdraw["annotations"],
    "notas":                  techdraw["annotations"],
    "texto":                  techdraw["annotations"],

    "sombreado":              techdraw["hatching"],
    "rayado":                 techdraw["hatching"],
    "hatch":                  techdraw["hatching"],
    "tramas":                 techdraw["hatching"],

    "vertices":               techdraw["addvertices"],
    "vértices":               techdraw["addvertices"],
    "vertice":                techdraw["addvertices"],
    "vértice":                techdraw["addvertices"],
    "agregar vértices":       techdraw["addvertices"],

    "otras vistas":           techdraw["otherviews"],
    "vistas auxiliares":      techdraw["otherviews"],
    "proyecciones":           techdraw["otherviews"],

    "caracteristicas":        techdraw["features"],
    "características":        techdraw["features"],
    "elementos":              techdraw["features"],

    "ayuda":                  techdraw["help"],
    "informacion":            techdraw["help"],
    "información":            techdraw["help"],
    "opciones":               techdraw["help"],
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

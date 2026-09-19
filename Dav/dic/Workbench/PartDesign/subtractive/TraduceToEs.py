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

from .subtractive import subtractive
from .ayuda import ayuda
from measure import CreateDimension

TraduceToEs = {
    # Pocket
    "vaciado": subtractive["pocket"],
    "corte": subtractive["pocket"],

    # Groove
    "ranura": subtractive["groove"],
    "canal": subtractive["groove"],

    # Hole
    "agujero": subtractive["hole"],
    "orificio": subtractive["hole"],

    # Subtractive Box
    "caja sustractiva": subtractive["subtractivebox"],

    # Subtractive Cone
    "cono sustractivo": subtractive["subtractivecone"],

    # Subtractive Cylinder
    "cilindro sustractivo": subtractive["subtractivecylinder"],

    # Subtractive Ellipsoid
    "elipsoide sustractivo": subtractive["subtractiveellipsoid"],

    # Subtractive Helix
    "helice sustractiva": subtractive["subtractivehelix"],

    # Subtractive Loft
    "recubrimiento sustractivo": subtractive["subtractiveloft"],

    # Subtractive Pipe
    "tuberia sustractiva": subtractive["subtractivepipe"],

    # Subtractive Prism
    "prisma sustractivo": subtractive["subtractiveprism"],

    # Subtractive Sphere
    "esfera sustractiva": subtractive["subtractivesphere"],

    # Subtractive Torus
    "toro sustractivo": subtractive["subtractivetorus"],

    # Subtractive Wedge
    "cuna sustractiva": subtractive["subtractivewedge"],

    # Boolean
    "booleano": subtractive["boolean"],
    "operacion booleana": subtractive["boolean"],

    # Cortes por medida dictada (sin dialogo)
    "vaciado por medida":    subtractive["pocket_by_length"],
    "vaciar por medida":     subtractive["pocket_by_length"],
    "hueco por medida":      subtractive["pocket_by_length"],

    "agujero por medidas":   subtractive["hole_by_size"],
    "perforar por medidas":  subtractive["hole_by_size"],
    "agujero por diametro":  subtractive["hole_by_size"],

    "ranura por angulo":     subtractive["groove_by_angle"],
    "ranurar por angulo":    subtractive["groove_by_angle"],

    # Cortes con primitivas por medidas dictadas
    "cortar caja por medidas":     subtractive["cut_box_by_size"],
    "restar caja por medidas":     subtractive["cut_box_by_size"],

    "cortar cilindro por medidas": subtractive["cut_cylinder_by_size"],
    "restar cilindro por medidas": subtractive["cut_cylinder_by_size"],

    "cortar esfera por radio":     subtractive["cut_sphere_by_radius"],

    # Help
    "ayuda": subtractive['help'],
    "información": subtractive['help'],
    "opciones": subtractive['help'],

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

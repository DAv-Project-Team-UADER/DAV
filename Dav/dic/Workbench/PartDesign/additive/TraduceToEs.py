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

from .additive import additive
from .ayuda import ayuda
from measure import CreateDimension

TraduceToEs = {
    # Rellenar
    "Rellenar":         additive["pad"],
    "Relleno":          additive["pad"],
    "Rellenar con":     additive["pad"],
    "Rellenar a":       additive["pad"],
    "Rellenar hasta":   additive["pad"],
    "extruir":          additive["pad"],
    "extrusion":        additive["pad"],
    "extrusión":        additive["pad"],
    "pad":              additive["pad"],

    # Transformacion
    "Transformación":   additive["revolution"],
    "Transformar":      additive["revolution"],
    "Transformar con":  additive["revolution"],
    "Transformar a":    additive["revolution"],
    "Transformar hasta":additive["revolution"],

    #Helice Aditiva
    "Hélice Aditiva":   additive["additivehelix"],
    "Hélice":           additive["additivehelix"],
    "Crear Hélice":     additive["additivehelix"],
    "Crear Hélice con": additive["additivehelix"],
    "Crear Hélice a":   additive["additivehelix"],
    "Crear Hélice hasta":additive["additivehelix"],

    #Sombreado aditivo
    "Sombreado Aditivo":   additive["additiveloft"],
    "Sombreado":           additive["additiveloft"],
    "Crear Sombreado":     additive["additiveloft"],
    "Crear Sombreado con": additive["additiveloft"],
    "Crear Sombreado a":   additive["additiveloft"],
    "Crear Sombreado hasta":additive["additiveloft"],

    #Tubo aditivo
    "Tubo Aditivo":   additive["additivepipe"],
    "Tubo":           additive["additivepipe"],
    "Crear Tubo":     additive["additivepipe"],
    "Crear Tubo con": additive["additivepipe"],
    "Crear Tubo a":   additive["additivepipe"],
    "Crear Tubo hasta":additive["additivepipe"],

    #Caja aditiva
    "Caja Aditiva":   additive["additivebox"],
    "Caja":           additive["additivebox"],
    "Crear Caja":     additive["additivebox"],
    "Crear Caja con": additive["additivebox"],
    "Crear Caja a":   additive["additivebox"],
    "Crear Caja hasta":additive["additivebox"],

    #Cono aditivo
    "Cono Aditivo":   additive["additivecone"],
    "Cono":           additive["additivecone"],
    "Crear Cono":     additive["additivecone"],
    "Crear Cono con": additive["additivecone"],
    "Crear Cono a":   additive["additivecone"],
    "Crear Cono hasta":additive["additivecone"],

    #Cilindro aditivo
    "Cilindro Aditivo":   additive["additivecylinder"],
    "Cilindro":           additive["additivecylinder"],
    "Crear Cilindro":     additive["additivecylinder"],
    "Crear Cilindro con": additive["additivecylinder"],
    "Crear Cilindro a":   additive["additivecylinder"],
    "Crear Cilindro hasta":additive["additivecylinder"],

    #Elipsoide aditivo
    "Elipsoide Aditivo":   additive["additiveellipsoid"],
    "Elipse estirada":           additive["additiveellipsoid"],
    "Crear Elipse estirada":     additive["additiveellipsoid"],
    "Crear Elipse estirada con": additive["additiveellipsoid"],
    "Crear Elipse estirada a":   additive["additiveellipsoid"],
    "Crear Elipse estirada hasta":additive["additiveellipsoid"],
    "elipse":            additive["additiveellipsoid"],
    "Elipsoide":       additive["additiveellipsoid"],

    #Prisma aditivo
    "Prisma Aditivo":   additive["additiveprism"],
    "Prisma":           additive["additiveprism"],
    "Crear Prisma":     additive["additiveprism"],
    "Crear Prisma con": additive["additiveprism"],
    "Crear Prisma a":   additive["additiveprism"],
    "Crear Prisma hasta":additive["additiveprism"],

    #Esfera aditiva
    "Esfera Aditiva":   additive["additivesphere"],
    "Esfera":           additive["additivesphere"],
    "Crear Esfera":     additive["additivesphere"],
    "Crear Esfera con": additive["additivesphere"],
    "Crear Esfera a":   additive["additivesphere"],
    "Crear Esfera hasta":additive["additivesphere"],
    "Bola"  :           additive["additivesphere"],
    "pelota":           additive["additivesphere"],

    #Toro aditivo
    "Toro Aditivo":   additive["additivetorus"],
    "Toro":           additive["additivetorus"],
    "Crear Toro":     additive["additivetorus"],
    "Crear Toro con": additive["additivetorus"],
    "Crear Toro a":   additive["additivetorus"],
    "Crear Toro hasta":additive["additivetorus"],

    #Cuña aditiva
    "Cuña Aditiva":   additive["additivewedge"],
    "Cuña":           additive["additivewedge"],
    "Crear Cuña":     additive["additivewedge"],
    "Crear Cuña con": additive["additivewedge"],
    "Crear Cuña a":   additive["additivewedge"],
    "Crear Cuña hasta":additive["additivewedge"],
    
    # pad_sketch
    "extruir boceto": additive["pad_sketch"],
    "extruir": additive["pad_sketch"],
    "dar alturara": additive["pad_sketch"],
    "dar volumen": additive["pad_sketch"],
    "dar profundidad": additive["pad_sketch"],
    "extender perfil": additive["pad_sketch"],
    "engrosar": additive["pad_sketch"],

    # loft_profiles
    "mezclar formas": additive["loft_profiles"],
    "barrer superficies": additive["loft_profiles"],
    "deformar secciones": additive["loft_profiles"],


    # Extrusion por medida dictada (sin dialogo)
    "extruir por medida": additive["pad_by_length"],
    "extruir por altura": additive["pad_by_length"],
    "extruir altura": additive["pad_by_length"],
    "dar altura": additive["pad_by_length"],

    # Caja por dimensiones dictadas
    "caja por medidas": additive["box_by_size"],
    "cubo por medidas": additive["box_by_size"],
    "crear caja por medidas": additive["box_by_size"],
    "caja por dimensiones": additive["box_by_size"],
    "cubo": additive["box_by_size"],
    "caja": additive["box_by_size"],
    "cuadrado": additive["box_by_size"],
    # Cilindro por dimensiones dictadas
    "cilindro por medidas": additive["cylinder_by_size"],
    "crear cilindro por medidas": additive["cylinder_by_size"],
    "cilindro por radio y altura": additive["cylinder_by_size"],

    # Revolucion por angulo dictado
    "revolucion por angulo": additive["revolve_by_angle"],
    "revolver por angulo": additive["revolve_by_angle"],
    "girar perfil": additive["revolve_by_angle"],

    # Primitivas por medidas dictadas
    "esfera por radio":      additive["sphere_by_radius"],
    "crear esfera por radio": additive["sphere_by_radius"],

    "cono por medidas":      additive["cone_by_size"],
    "crear cono por medidas": additive["cone_by_size"],

    "toro por medidas":      additive["torus_by_size"],
    "rosquilla por medidas": additive["torus_by_size"],

    "prisma por medidas":    additive["prism_by_size"],
    "crear prisma por medidas": additive["prism_by_size"],

    #Ayuda
    "ayuda":                additive["help"],
    "información":          additive["help"],
    "opciones":             additive["help"]
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

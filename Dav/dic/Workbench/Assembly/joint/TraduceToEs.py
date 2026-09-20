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

"""Spanish spoken-word mapping for the DAV joint dictionary."""

from .joint import joint
from .ayuda import ayuda

TraduceToEs = {

    # Ángulo
    "union angular": joint["angle"],
    "unión angular": joint["angle"],
    "junta angular": joint["angle"],
    "union de angulo": joint["angle"],
    "unión de ángulo": joint["angle"],
    "restriccion de angulo": joint["angle"],
    "restricción de ángulo": joint["angle"],
    "angulo": joint["angle"],
    "ángulo": joint["angle"],

    # Rótula / Esférica
    "union esferica": joint["ball"],
    "unión esférica": joint["ball"],
    "junta esferica": joint["ball"],
    "junta esférica": joint["ball"],
    "union de esfera": joint["ball"],
    "unión de esfera": joint["ball"],
    "junta de esfera": joint["ball"],
    "rotula": joint["ball"],
    "rótula": joint["ball"],
    "union de rotula": joint["ball"],
    "unión de rótula": joint["ball"],
    "esferica": joint["ball"],
    "esférica": joint["ball"],

    # Paralela
    "union paralela": joint["parallel"],
    "unión paralela": joint["parallel"],
    "junta paralela": joint["parallel"],
    "union de paralelismo": joint["parallel"],
    "unión de paralelismo": joint["parallel"],
    "restriccion de paralelismo": joint["parallel"],
    "restricción de paralelismo": joint["parallel"],
    "paralela": joint["parallel"],
    "paralelo": joint["parallel"],
    "paralelismo": joint["parallel"],

    # Perpendicular
    "union perpendicular": joint["perpendicular"],
    "unión perpendicular": joint["perpendicular"],
    "junta perpendicular": joint["perpendicular"],
    "union de perpendicularidad": joint["perpendicular"],
    "unión de perpendicularidad": joint["perpendicular"],
    "restriccion de perpendicularidad": joint["perpendicular"],
    "restricción de perpendicularidad": joint["perpendicular"],
    "perpendicular": joint["perpendicular"],

    # Correa / Cadena
    "union de correa": joint["belt"],
    "unión de correa": joint["belt"],
    "junta de correa": joint["belt"],
    "union correa": joint["belt"],
    "unión correa": joint["belt"],
    "correa": joint["belt"],
    "union de cadena": joint["belt"],
    "unión de cadena": joint["belt"],
    "junta de cadena": joint["belt"],
    "union cadena": joint["belt"],
    "unión cadena": joint["belt"],
    "cadena": joint["belt"],

    # Engranajes
    "union de engranajes": joint["gears"],
    "unión de engranajes": joint["gears"],
    "union de engranaje": joint["gears"],
    "unión de engranaje": joint["gears"],
    "junta de engranajes": joint["gears"],
    "junta de engranaje": joint["gears"],
    "union engranajes": joint["gears"],
    "unión engranajes": joint["gears"],
    "engranajes": joint["gears"],
    "engranaje": joint["gears"],

    # Piñón-cremallera
    "union pinon cremallera": joint["rackpinion"],
    "unión piñón cremallera": joint["rackpinion"],
    "union piñon cremallera": joint["rackpinion"],
    "unión piñon cremallera": joint["rackpinion"],
    "union piñón cremallera": joint["rackpinion"],
    "junta piñón cremallera": joint["rackpinion"],
    "junta piñon cremallera": joint["rackpinion"],
    "union de piñon y cremallera": joint["rackpinion"],
    "unión de piñón y cremallera": joint["rackpinion"],
    "piñon cremallera": joint["rackpinion"],
    "piñón cremallera": joint["rackpinion"],
    "piñon y cremallera": joint["rackpinion"],
    "piñón y cremallera": joint["rackpinion"],
    "cremallera": joint["rackpinion"],

    # Helicoidal / Tornillo
    "union helicoidal": joint["screw"],
    "unión helicoidal": joint["screw"],
    "junta helicoidal": joint["screw"],
    "union de tornillo": joint["screw"],
    "unión de tornillo": joint["screw"],
    "junta de tornillo": joint["screw"],
    "tornillo": joint["screw"],
    "tornillo de avance": joint["screw"],
    "helicoidal": joint["screw"],

    # Cilíndrica
    "union cilindrica": joint["cylindrical"],
    "unión cilíndrica": joint["cylindrical"],
    "junta cilindrica": joint["cylindrical"],
    "junta cilíndrica": joint["cylindrical"],
    "union de cilindro": joint["cylindrical"],
    "unión de cilindro": joint["cylindrical"],
    "cilindrica": joint["cylindrical"],
    "cilíndrica": joint["cylindrical"],
    "cilindrico": joint["cylindrical"],
    "cilíndrico": joint["cylindrical"],

    # Distancia
    "union de distancia": joint["distance"],
    "unión de distancia": joint["distance"],
    "junta de distancia": joint["distance"],
    "restriccion de distancia": joint["distance"],
    "restricción de distancia": joint["distance"],
    "distancia": joint["distance"],

    # Fija
    "union fija": joint["fixed"],
    "unión fija": joint["fixed"],
    "junta fija": joint["fixed"],
    "union de fijacion": joint["fixed"],
    "unión de fijación": joint["fixed"],
    "junta de fijacion": joint["fixed"],
    "junta de fijación": joint["fixed"],
    "fijar": joint["fixed"],
    "fijo": joint["fixed"],
    "fija": joint["fixed"],

    # Revolución / Bisagra
    "union de revolucion": joint["revolute"],
    "unión de revolución": joint["revolute"],
    "junta de revolucion": joint["revolute"],
    "junta de revolución": joint["revolute"],
    "union revoluta": joint["revolute"],
    "unión revoluta": joint["revolute"],
    "junta revoluta": joint["revolute"],
    "revoluta": joint["revolute"],
    "revolucion": joint["revolute"],
    "revolución": joint["revolute"],
    "bisagra": joint["revolute"],

    # Deslizante / Prismática
    "union deslizante": joint["slider"],
    "unión deslizante": joint["slider"],
    "junta deslizante": joint["slider"],
    "union de deslizamiento": joint["slider"],
    "unión de deslizamiento": joint["slider"],
    "junta de deslizamiento": joint["slider"],
    "union prismatica": joint["slider"],
    "unión prismática": joint["slider"],
    "junta prismatica": joint["slider"],
    "junta prismática": joint["slider"],
    "deslizante": joint["slider"],
    "prismatica": joint["slider"],
    "prismática": joint["slider"],

    # Ayuda / Soporte
    "ayuda": joint["help"],
    "informacion": joint["help"],
    "información": joint["help"],
    "opciones": joint["help"]
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

# Cota / medir
from measure import CreateDimension, MEASURE_PHRASES
for _phrase in MEASURE_PHRASES['es']:
    TraduceToEs.setdefault(_phrase, CreateDimension)

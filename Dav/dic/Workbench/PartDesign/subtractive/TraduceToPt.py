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

"""Portuguese spoken-word mapping for PartDesign subtractive commands."""

from .subtractive import subtractive
from .ayuda import ayuda
from measure import CreateDimension

TraduceToPt = {
    # Pocket
    "bolso": subtractive["pocket"],
    "corte": subtractive["pocket"],

    # Groove
    "ranhura": subtractive["groove"],
    "canal": subtractive["groove"],

    # Hole
    "furo": subtractive["hole"],
    "perfuração": subtractive["hole"],

    # Subtractive Box
    "caixa sustractiva": subtractive["subtractivebox"],
    "corte caixa": subtractive["subtractivebox"],

    # Subtractive Cone
    "cono sustractivo": subtractive["subtractivecone"],
    "corte cono": subtractive["subtractivecone"],

    # Subtractive Cylinder
    "cilindro sustractivo": subtractive["subtractivecylinder"],
    "corte cilindro": subtractive["subtractivecylinder"],

    # Subtractive Ellipsoid
    "elipsoide sustractivo": subtractive["subtractiveellipsoid"],
    "corte elipsoide": subtractive["subtractiveellipsoid"],

    # Subtractive Helix
    "helice subtrativa": subtractive["subtractivehelix"],
    "corte helice": subtractive["subtractivehelix"],

    # Subtractive Loft
    "loft sustractivo": subtractive["subtractiveloft"],
    "corte loft": subtractive["subtractiveloft"],

    # Subtractive Pipe
    "tubo sustractivo": subtractive["subtractivepipe"],
    "corte tubo": subtractive["subtractivepipe"],

    # Subtractive Prism
    "prisma sustractivo": subtractive["subtractiveprism"],
    "corte prisma": subtractive["subtractiveprism"],

    # Subtractive Sphere
    "esfera sustractiva": subtractive["subtractivesphere"],
    "corte esfera": subtractive["subtractivesphere"],

    # Subtractive Torus
    "toro sustractivo": subtractive["subtractivetorus"],
    "corte toro": subtractive["subtractivetorus"],

    # Subtractive Wedge
    "cuna sustractiva": subtractive["subtractivewedge"],
    "corte cuna": subtractive["subtractivewedge"],

    # Boolean
    "booleano": subtractive["boolean"],
    "operação booleana": subtractive["boolean"],

    # Cortes por medida ditada (sem dialogo)
    "vazio por medida":      subtractive["pocket_by_length"],
    "esvaziar por medida":   subtractive["pocket_by_length"],

    "furo por medidas":      subtractive["hole_by_size"],
    "perfurar por medidas":  subtractive["hole_by_size"],
    "furo cego":             subtractive["blind_hole"],
    "furo cego por medidas": subtractive["blind_hole"],
    "buraco cego":           subtractive["blind_hole"],

    "ranhura por angulo":    subtractive["groove_by_angle"],

    # Cortes com primitivas por medidas ditadas
    "cortar caixa por medidas":    subtractive["cut_box_by_size"],
    "cortar cilindro por medidas": subtractive["cut_cylinder_by_size"],
    "cortar esfera por raio":      subtractive["cut_sphere_by_radius"],

    # Help
    "ajuda": subtractive['help'],
    "informação": subtractive['help'],
    "opções": subtractive['help'],

    # MEASURE
    "medir": CreateDimension,
    "medida": CreateDimension,
    "medir distancia": CreateDimension,
    "medir distância": CreateDimension,
    "distância": CreateDimension,
    "distancia": CreateDimension,
    "cotar": CreateDimension,
    "dimensionar": CreateDimension,
    "aferir": CreateDimension,
    "mensurar": CreateDimension,
    "calcular distância": CreateDimension,
    "calcular distancia": CreateDimension,
    "comprimento": CreateDimension,
    "separação": CreateDimension,
    "separacao": CreateDimension,
    "afastamento": CreateDimension,
    "extensão": CreateDimension,
    "extensao": CreateDimension,
    "cota": CreateDimension,
    "cotagem": CreateDimension,
    "acotação": CreateDimension,
    "acotacao": CreateDimension,
    "dimensão": CreateDimension,
    "dimensao": CreateDimension,
    "métrica": CreateDimension,
    "metrica": CreateDimension,
    "dimensionamento": CreateDimension,
    "metro": CreateDimension,
    "milímetro": CreateDimension,
    "milimetro": CreateDimension,
    "centímetro": CreateDimension,
    "centimetro": CreateDimension,
    "flexômetro": CreateDimension,
    "flexometro": CreateDimension,
    "metro enrolável": CreateDimension,
    "metro enrolavel": CreateDimension,
    "régua": CreateDimension,
    "regua": CreateDimension,
    "escalímetro": CreateDimension,
    "escalimetro": CreateDimension,
    "calibre": CreateDimension,
    "paquímetro": CreateDimension,
    "paquimetro": CreateDimension,
    "micrômetro": CreateDimension,
    "micrometro": CreateDimension,
    "tolerância": CreateDimension,
    "tolerancia": CreateDimension,
    "desvio": CreateDimension,
    "ajuste": CreateDimension,
    "medição": CreateDimension,
    "medicao": CreateDimension,
    "mensuração": CreateDimension,
    "mensuracao": CreateDimension,
    "aferição": CreateDimension,
    "afericao": CreateDimension,
    "calibração": CreateDimension,
    "calibracao": CreateDimension,
    "verificação": CreateDimension,
    "verificacao": CreateDimension,
    "inspeção": CreateDimension,
    "inspecao": CreateDimension,
    "controle dimensional": CreateDimension,
    "metrologia": CreateDimension,
}

from dic.StdView.StandardViews.StandardViews import *

TraduceToPt.update ({
    # bottom
    'baixo':                StandardViews['bottom'],
    'inferior':             StandardViews['bottom'],
    'vista baixo':          StandardViews['bottom'],
    'vista de baixo':          StandardViews['bottom'],
    'vista inferior':       StandardViews['bottom'],
    'parte inferior':       StandardViews['bottom'],
    'de baixo':             StandardViews['bottom'],

    # boxzoom
    'zoom caixa':           StandardViews['boxzoom'],
    'zoom retangular':      StandardViews['boxzoom'],
    'zoom area':            StandardViews['boxzoom'],
    'zoom por caixa':       StandardViews['boxzoom'],
    'zoom de area':         StandardViews['boxzoom'],
    'zoom de área':         StandardViews['boxzoom'],
    'janela de zoom':      StandardViews['boxzoom'],
    'zoom por janela':     StandardViews['boxzoom'],

    # newview
    'nova vista':           StandardViews['newview'],
    'criar vista':          StandardViews['newview'],
    'janela nova':          StandardViews['newview'],
    'nova janela':          StandardViews['newview'],
    'abrir nova vista':     StandardViews['newview'],
    'criar nova vista':     StandardViews['newview'],
    'nova visualização':    StandardViews['newview'],

    # dimetric
    'dimetrica':            StandardViews['dimetric'],
    'dimétrica':            StandardViews['dimetric'],
    'vista dimetrica':      StandardViews['dimetric'],
    'vista dimétrica':      StandardViews['dimetric'],
    'projecao dimetrica':   StandardViews['dimetric'],
    'projeção dimétrica': StandardViews['dimetric'], 

    # fitall
    'ajustar tudo':         StandardViews['fitall'],
    'enquadrar tudo':       StandardViews['fitall'],
    'ver tudo':             StandardViews['fitall'],
    'zoom tudo':            StandardViews['fitall'],
    'ajustar a tudo':       StandardViews['fitall'],
    'mostrar tudo':         StandardViews['fitall'],
    'encaixar tudo':        StandardViews['fitall'],
    'enquadrar modelo':     StandardViews['fitall'],
    'mostrar seleção':      StandardViews['fitselection'],
    'encaixar seleção':     StandardViews['fitselection'],
    'focar seleção':        StandardViews['fitselection'],

    # fitselection
    'ajustar selecao':      StandardViews['fitselection'],
    'ajustar seleção':      StandardViews['fitselection'],
    'enquadrar selecao':    StandardViews['fitselection'],
    'enquadrar seleção':    StandardViews['fitselection'],
    'zoom selecao':         StandardViews['fitselection'],
    'zoom seleção':         StandardViews['fitselection'],

    # front
    'frontal':              StandardViews['front'],
    'frente':               StandardViews['front'],
    'vista frontal':        StandardViews['front'],
    'de frente':            StandardViews['front'],
    'vista de frente':      StandardViews['front'],

    # fullscreen
    'tela cheia':           StandardViews['fullscreen'],
    'ecra completo':        StandardViews['fullscreen'],
    'ecrã completo':        StandardViews['fullscreen'],
    'maximizar vista':      StandardViews['fullscreen'],
    'modo tela cheia':      StandardViews['fullscreen'],
    'maximizar':            StandardViews['fullscreen'],
    'tela completa':        StandardViews['fullscreen'],
    'modo completo':        StandardViews['fullscreen'],

    # home
    'inicio':               StandardViews['home'],
    'início':               StandardViews['home'],
    'vista inicial':        StandardViews['home'],
    'vista padrao':         StandardViews['home'],
    'vista padrão':         StandardViews['home'],
    'restaurar vista':      StandardViews['home'],

    # isometric
    'isometrica':           StandardViews['isometric'],
    'isométrica':           StandardViews['isometric'],
    'vista isometrica':     StandardViews['isometric'],
    'vista isométrica':     StandardViews['isometric'],
    'projecao isometrica':  StandardViews['isometric'],
    'projeção isométrica': StandardViews['isometric'],

    # left
    'esquerda':             StandardViews['left'],
    'esquerdo':             StandardViews['left'],
    'vista esquerda':       StandardViews['left'],
    'lateral esquerdo':     StandardViews['left'],
    'da esquerda':          StandardViews['left'],
    'lado esquerdo':        StandardViews['left'],
    'vista lateral esquerda': StandardViews['left'],

    # rear
    'traseira':             StandardViews['rear'],
    'atras':                StandardViews['rear'],
    'atrás':                StandardViews['rear'],
    'vista traseira':       StandardViews['rear'],
    'posterior':            StandardViews['rear'],
    'de tras':              StandardViews['rear'],
    'vista posterior':      StandardViews['rear'],
    'vista de trás':        StandardViews['rear'],

    # right
    'direita':              StandardViews['right'],
    'direito':              StandardViews['right'],
    'vista direita':        StandardViews['right'],
    'lateral direito':      StandardViews['right'],
    'da direita':           StandardViews['right'],
    'lado direito':         StandardViews['right'],
    'vista lateral direita':StandardViews['right'],

    # top
    'topo':                 StandardViews['top'],
    'superior':             StandardViews['top'],
    'vista superior':       StandardViews['top'],
    'planta':               StandardViews['top'],
    'de cima':              StandardViews['top'],
    'vista de cima':        StandardViews['top'],
    'vista topo':           StandardViews['top'],
    'vista superior':       StandardViews['top'],
    'vista em planta':      StandardViews['top'],

    # trimetric
    'trimetrica':           StandardViews['trimetric'],
    'trimétrica':           StandardViews['trimetric'],
    'vista trimetrica':     StandardViews['trimetric'],
    'vista trimétrica':     StandardViews['trimetric'],
    'projecao trimetrica':  StandardViews['trimetric'],
    'projeção trimétrica':  StandardViews['trimetric'],

    # zoomin
    'aproximar':            StandardViews['zoomin'],
    'zoom aproximar':       StandardViews['zoomin'],
    'aumentar zoom':        StandardViews['zoomin'],
    'zoom mais':            StandardViews['zoomin'],
    'ampliar':              StandardViews['zoomin'],
    'zoom in':              StandardViews['zoomin'],
    'mais zoom':            StandardViews['zoomin'],

    # zoomout
    'afastar':              StandardViews['zoomout'],
    'zoom afastar':         StandardViews['zoomout'],
    'diminuir zoom':        StandardViews['zoomout'],
    'zoom menos':           StandardViews['zoomout'],
    'reduzir zoom':         StandardViews['zoomout'],
    'zoom out':             StandardViews['zoomout'],
    'menos zoom':           StandardViews['zoomout'],

})

# Mover la vista (centra la cámara en un punto)
from moveview import MoveView, MOVE_VIEW_PHRASES
for _phrase in MOVE_VIEW_PHRASES['pt']:
    TraduceToPt.setdefault(_phrase, MoveView)

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

"""Mapeamento de palavras em portugues para o dicionario DAV AssemblyWorkbench."""
 
from .Assembly import assembly
from .joint.joint import joint
from .ayuda import ayuda
 
TraduceToPt = {
    "novo conjunto":       assembly["create"],
    "criar conjunto":      assembly["create"],
    "nova peça":           assembly["newpart"],
    "inserir peça":        assembly["newpart"],
    "inserir link":        assembly["link"],
    "vincular peça":       assembly["link"],
    "resolver":            assembly["solve"],
    "resolver conjunto":   assembly["solve"],
    "fixar":      assembly["solve"],
    "montar conjunto":     assembly["create"],
    "fazer conjunto":         assembly["solve"],
    "verificar conjunto":     assembly["solve"],
    "conjunto":              assembly["create"],
    "arranjo":                assembly["solve"],
    
    "vista explodida":     assembly["view"],
    "explodir vista":      assembly["view"],
    "explodir":   assembly["view"],
    "criar vista":         assembly["view"],
    "simulação":           assembly["simulation"],
    "criar simulação":     assembly["simulation"],
    "lista de materiais":  assembly["bom"],
    "bom":                 assembly["bom"],
    "lista":               assembly["bom"],
    "materiais":           assembly["bom"],
    "preferências":        assembly["preferences"],
    "configurações":       assembly["preferences"],
    "fixar peça":          assembly["grounded"],
    "ancora":              assembly["grounded"],
    "junta":               joint,
    "vincular peças":        joint,
    "vincular partes":       joint,
    "vincular":             joint,
    "juntar":               joint,
    "unir":                joint,
    "conectar":            joint,
    "junto":                joint,

    # Juntas por voz (sem dialogo)
    "junta fixa":            assembly["fixed_joint"],
    "fixar pecas":           assembly["fixed_joint"],

    "junta giratoria":       assembly["revolute_joint"],
    "dobradica":             assembly["revolute_joint"],

    "junta deslizante":      assembly["slider_joint"],
    "deslizar pecas":        assembly["slider_joint"],

    "junta por distancia":   assembly["distance_joint"],
    "separar pecas":         assembly["distance_joint"],

    "junta por angulo":      assembly["angle_joint"],
    "angulo entre pecas":    assembly["angle_joint"],

    "fixar ao chao":         assembly["ground_part"],
    "ancorar peca":          assembly["ground_part"],

    # Juntas restantes por voz
    "junta esferica":        assembly["ball_joint"],
    "rotula":                assembly["ball_joint"],
    "junta cilindrica":      assembly["cylindrical_joint"],
    "junta paralela":        assembly["parallel_joint"],
    "junta perpendicular":   assembly["perpendicular_joint"],

    "junta de engrenagens":  assembly["gears_joint"],
    "junta de correia":      assembly["belt_joint"],
    "junta de parafuso":     assembly["screw_joint"],
    "junta de cremalheira":  assembly["rack_pinion_joint"],

    "ajuda":               joint['help'],
    "informação":          joint['help'],
    "opções":              joint['help']
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

    # help
    'ajuda':                StandardViews['help'],
    "informação":           StandardViews['help'],
    'opções':               StandardViews['help'],
})

# Cota / medir
from measure import CreateDimension, MEASURE_PHRASES
for _phrase in MEASURE_PHRASES['pt']:
    TraduceToPt.setdefault(_phrase, CreateDimension)

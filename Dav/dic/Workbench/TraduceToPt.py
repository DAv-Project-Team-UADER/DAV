# Copyright (C) 2026 El Equipo del Projeto DAV
# Copyright (C) 2026 The DAV Project Team
# Universidad Autónoma de Entre Ríos (UADER)
# Sob a direção de Guillermo Gerard e Gallo Fabricio David
#
# Este programa é software livre: você pode redistribuir e/ou modificar
# sob os termos da Licença Pública Geral GNU conforme publicado
# pela Fundação para o Software Livre, na versão 3 da Licença.
#
# Este programa é distribuído na esperança de ser útil,
# mas SEM QUALQUER GARANTIA; mesmo sem a garantia implícita de
# COMERCIALIZAÇÃO ou ADEQUAÇÃO PARA UM PROPÓSITO ESPECÍFICO. Consulte
# a Licença Pública Geral GNU para mais detalhes.
#
# Você deveria ter recebido uma cópia da Licença Pública Geral GNU
# junto com este programa. Se não, consulte <http://www.gnu.org/licenses/>.
# SPDX-License-Identifier: GPL-3.0-or-later

"""Mapeamento de palavras em Português para o dicionário DAV Workbench."""
from .workbench import workbench
from .Assembly.Assembly import assembly
from .DraftWork.DraftWork import draft
from .Part.Part import part
from .PartDesign.partdesign import partdesign
from .Sketcher.sketcher import sketcher
from .TechDraw.TechDraw import techdraw

TraduceToPt = {
    # Bancada de Montagem
    "montagem":          assembly,
    "montagens":         assembly,
    "conjunto":          assembly,
    "conjuntos":         assembly,
    "bancada de montagem": assembly,
    "bancada de conjunto": assembly,
    "banco de montagem":   assembly,
    "articular":          assembly,
    "juntar":             assembly,
    "juntar peças":        assembly,

    # Bancada de Desenho
    "desenho":           draft,
    "desenhos":          draft,
    "bancada de desenho": draft,
    
    "rascunho":          draft,
    "rascunhos":         draft,
    "draftwork":         draft,
    "draft":             draft,
    "desenhar":          draft,
    

    # Bancada de Peça
    "peça":              part,
    "peças":             part,
    "bancada de peça":   part,
    "bancada de peças":  part,
    "parte":             part,
    "partes":            part,
    "pedaço":            part,
    "pedaços":           part,
    

    # Bancada de Design de Peças
    "desenho de peça":    partdesign,
    "desenho de peças":   partdesign,
    "designer de peças": partdesign,
    "desenhista":        partdesign,
    "design":            partdesign,
    "bancada de design": partdesign,
    "partdesign":        partdesign,
    "part design":       partdesign,
    "projeto de peça":     partdesign,
    "projeto de peças":    partdesign,
    

    # Bancada de Esboço
   
    "banco de esboço":   sketcher,
    "desenhar esboço":   sketcher,
    "sketcher":          sketcher,
    "croqui":            sketcher,
    "croquis":           sketcher,
    "esboço":            sketcher,
    "esboços":           sketcher,
    # Bancada de Desenho Técnico
    "desenho técnico":   techdraw,
    "desenhos técnicos": techdraw,
    "bancada de desenho técnico": techdraw,
    "techdraw":          techdraw,
    "desenho de planos": techdraw,
    "planos":            techdraw,
    "esboço técnico":    techdraw,
    "rótulo":             techdraw,
    "rótulos":            techdraw,
    "técnico":             techdraw,

    "ajuda":             workbench["help"],
    "informação":        workbench["help"],
    "opções":            workbench["help"],
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
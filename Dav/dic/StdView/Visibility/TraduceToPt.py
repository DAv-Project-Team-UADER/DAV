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

"""Mapeamento de palavras faladas em português para a pasta de dicionários DAV StdView/Visibility."""

from .Visibility import visibility

TraduceToPt = {
    "ocultar objetos":      visibility["hideobjects"],
    "ocultar":              visibility["hide"],
    "todos os links":      visibility["alllinks"],
    "vinculado":            visibility["linked"],
    "vínculo final":        visibility["linkedfinal"],
    "voltar atrás":         visibility["selback"],
    "caixa de limites":     visibility["boundingbox"],
    "avançar seleção":      visibility["selforward"],
    "selecionar visíveis":  visibility["selectvisible"],
    "mostrar objetos":      visibility["showobjects"],
    "mostrar":              visibility["show"],
    "alternar tudo":        visibility["toggleall"],
    "selecionabilidade":    visibility["selectability"],
    "transparência":        visibility["transparency"],
    "alternar":             visibility["toggle"],
    "alinhar à seleção":    visibility["aligntoselection"],

    "ocultar objetos":      visibility["hideobjects"],
    "ocultar tudo":         visibility["hideobjects"],
    "esconder objetos":     visibility["hideobjects"],
    "esconder tudo":        visibility["hideobjects"],

    "ocultar":              visibility["hide"],
    "esconder":             visibility["hide"],
    "ocultar selecao":      visibility["hide"],
    "ocultar seleção":      visibility["hide"],
    "esconder selecao":     visibility["hide"],
    "esconder seleção":     visibility["hide"],

    "todos os links":      visibility["alllinks"],
    "todos os elos":        visibility["alllinks"],
    "selecionar todos os links": visibility["alllinks"],
    "selecionar todos os elos": visibility["alllinks"],

    "vinculado":            visibility["linked"],
    "objeto vinculado":     visibility["linked"],
    "enlaçado":             visibility["linked"],
    "ir para o link":       visibility["linked"],
    "ir para o elo":        visibility["linked"],

    "link final":           visibility["linkedfinal"],
    "elo final":            visibility["linkedfinal"],
    "vinculo final":        visibility["linkedfinal"],
    "vínculo final":        visibility["linkedfinal"],
    "vinculado final":      visibility["linkedfinal"],

    "voltar selecao":       visibility["selback"],
    "voltar seleção":       visibility["selback"],
    "retroceder selecao":   visibility["selback"],
    "retroceder seleção":   visibility["selback"],
    "selecao anterior":     visibility["selback"],
    "seleção anterior":     visibility["selback"],

    "caixa delimitadora":   visibility["boundingbox"],
    "caixa de limites":     visibility["boundingbox"],
    "caixa limite":         visibility["boundingbox"],

    "avancar selecao":      visibility["selforward"],
    "avançar seleção":      visibility["selforward"],
    "avançar selecao":      visibility["selforward"],
    "avancar seleção":      visibility["selforward"],
    "proxima selecao":      visibility["selforward"],
    "próxima seleção":      visibility["selforward"],

    "selecionar visiveis":   visibility["selectvisible"],
    "selecionar visíveis":   visibility["selectvisible"],
    "selecionar objetos visiveis": visibility["selectvisible"],
    "selecionar objetos visíveis": visibility["selectvisible"],

    "mostrar objetos":      visibility["showobjects"],
    "mostrar tudo":         visibility["showobjects"],
    "exibir objetos":       visibility["showobjects"],
    "exibir tudo":          visibility["showobjects"],

    "mostrar":              visibility["show"],
    "exibir":               visibility["show"],
    "revelar":              visibility["show"],
    "mostrar selecao":      visibility["show"],
    "mostrar seleção":      visibility["show"],
    "exibir selecao":       visibility["show"],
    "exibir seleção":       visibility["show"],

    "alternar tudo":        visibility["toggleall"],
    "comutar tudo":         visibility["toggleall"],
    "alternar todos":       visibility["toggleall"],

    "selecionabilidade":    visibility["selectability"],
    "alternar selecionabilidade": visibility["selectability"],
    "permitir selecao":     visibility["selectability"],
    "permitir seleção":     visibility["selectability"],

    "transparencia":        visibility["transparency"],
    "transparência":        visibility["transparency"],
    "alternar transparencia": visibility["transparency"],
    "alternar transparência": visibility["transparency"],
    "transparente":         visibility["transparency"],

    "alternar":             visibility["toggle"],
    "alternar visibilidade": visibility["toggle"],
    "comutar visibilidade":  visibility["toggle"],

    "alinhar a selecao":    visibility["aligntoselection"],
    "alinhar à seleção":    visibility["aligntoselection"],
    "alinhar com selecao":  visibility["aligntoselection"],
    "alinhar com seleção":  visibility["aligntoselection"],
    "perpendicular à seleção": visibility["aligntoselection"],

    "ajuda":                visibility["help"],
    "informação":           visibility["help"],
    "opções":               visibility["help"],
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

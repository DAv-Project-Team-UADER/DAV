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

from .Toolbars import toolbars
from .Toolbars import toolbars as Toolbars
from .ayuda import ayuda

TraduceToPt = {

    # Área de transferência
    "área de transferência": toolbars["clipboard"],
    "area de transferencia": toolbars["clipboard"],
    "parte de transferência": toolbars["clipboard"],
    "a transferir": toolbars["clipboard"],
    "transferir": toolbars["clipboard"],
    "barra da área de transferência": toolbars["clipboard"],
    "ferramentas": toolbars["clipboard"],
    "copiar": toolbars["clipboard"],
    "colar": toolbars["clipboard"],
    "recortar": toolbars["clipboard"],
    "desfazer": toolbars["clipboard"],
    "refazer": toolbars["clipboard"],

    # Editar
    "editar": toolbars["edit"],
    "edição": toolbars["edit"],
    "edicao": toolbars["edit"],
    "barra de edição": toolbars["edit"],
    "barra de edicao": toolbars["edit"],

    # Arquivo
    "arquivo": toolbars["file"],
    "folha": toolbars["file"],
    "barra de arquivo": toolbars["file"],
    "barra de arquivos": toolbars["file"],

    # Barra de ajuda
    "barra de ajuda": toolbars["toolbarshelp"],
    "ajuda da barra": toolbars["toolbarshelp"],

    # Vistas
    "vistas": toolbars["views"],
    "vistas individuais": toolbars["views"],
    "perspectivas bidimensionais": toolbars["views"],
    "perspectiva da planta": toolbars["views"],
    "planta": toolbars["views"],
    "perspectiva lateral": toolbars["views"],
    "lateral": toolbars["views"],
    "perspectiva frontal": toolbars["views"],
    "frontal": toolbars["views"],
    "barra de vistas": toolbars["views"],

    # Bloquear barras
    "bloquear": toolbars["lock"],
    "bloquear barra": toolbars["lock"],
    "bloquear barras": toolbars["lock"],
    "desbloquear barra": toolbars["lock"],
    "desbloquear barras": toolbars["lock"],

    # Macro
    "macro": toolbars["macro"],
    "macros": toolbars["macro"],
    "barra de macros": toolbars["macro"],
    "criar macro": toolbars["macro"],
    "gravar macro": toolbars["macro"],

    # Estrutura
    "estrutura": toolbars["structure"],
    "barra de estrutura": toolbars["structure"],
    "organização": toolbars["structure"],
    
    # Vista
    "vista": toolbars["view"],
    "barra de vista": toolbars["view"],
    "ver": toolbars["view"],
    "visualizar": toolbars["view"],
    "visualização": toolbars["view"],

    # Bancada
    "bancada": toolbars["workbench"],
    "barra da bancada": toolbars["workbench"],
    "workbench": toolbars["workbench"],
    "bancadas": toolbars["workbench"],
    "iniciar bancada": toolbars["workbench"],
    "iniciar workbench": toolbars["workbench"],
    
    # Ajuda
    "ajuda": Toolbars["help"],
    "informação": Toolbars["help"],
    "opções": Toolbars["help"],
    
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

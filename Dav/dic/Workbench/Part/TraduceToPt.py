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

"""Portuguese spoken-word mapping for the DAV PartWorkbench dictionary."""

from .Part import part as Part

from .box.box import box
from .circle.circle import circle
from .cone.cone import cone
from .cube.cube import cube
from .cylinder.cylinder import cylinder
from .ellipse.ellipse import ellipse
from .line.line import line
from .new_sketch.new_sketch import new_sketch
from .part_chamfer.part_chamfer import part_chamfer
from .part_color_per_face.part_color_per_face import part_color_per_face
from .part_cross_sections.part_cross_sections import part_cross_sections
from .part_extrude.part_extrude import part_extrude
from .part_fillet.part_fillet import part_fillet
from .part_loft.part_loft import part_loft
from .part_makeface.part_makeface import part_makeface
from .part_mirror.part_mirror import part_mirror
from .part_offset.part_offset import part_offset
from .part_offset2d.part_offset2d import part_offset2d
from .part_projection_on_surface.part_projection_on_surface import part_projection_on_surface
from .part_revolve.part_revolve import part_revolve
from .part_ruled_surface.part_ruled_surface import part_ruled_surface
from .part_scale.part_scale import part_scale
from .part_section.part_section import part_section
from .part_sweep.part_sweep import part_sweep

from .ayuda import ayuda
from measure import CreateDimension

TraduceToPt = {
    "caixa": box["box"],
    "criar caixa": box["box"],
    "fazer caixa": box["box"],

    "circulo": circle["circle"],
    "círculo": circle["circle"],
    "criar circulo": circle["circle"],
    "criar círculo": circle["circle"],

    "cone": cone["cone"],
    "criar cone": cone["cone"],
    "cone primitivo": cone["cone"],

    "cubo": cube["cube"],
    "criar cubo": cube["cube"],
    "fazer cubo": cube["cube"],

    "cilindro": cylinder["cylinder"],
    "criar cilindro": cylinder["cylinder"],
    "cilindro primitivo": cylinder["cylinder"],

    "elipse": ellipse["ellipse"],
    "criar elipse": ellipse["ellipse"],
    "fazer elipse": ellipse["ellipse"],

    "linha": line["line"],
    "criar linha": line["line"],
    "fazer linha": line["line"],

    "novo sketch": new_sketch["new sketch"],
    "novo esboco": new_sketch["new sketch"],
    "novo esboço": new_sketch["new sketch"],
    "criar sketch": new_sketch["new sketch"],
    "criar esboco": new_sketch["new sketch"],
    "criar esboço": new_sketch["new sketch"],

    "chanfro": part_chamfer["chaflan"],
    "criar chanfro": part_chamfer["chaflan"],
    "bisel": part_chamfer["chaflan"],
    "biselar": part_chamfer["chaflan"],

    "cor por face": part_color_per_face["paint face"],
    "pintar face": part_color_per_face["paint face"],
    "colorir face": part_color_per_face["paint face"],

    "secoes transversais": part_cross_sections["cross sections"],
    "seções transversais": part_cross_sections["cross sections"],
    "cortes transversais": part_cross_sections["cross sections"],
    "criar secoes transversais": part_cross_sections["cross sections"],
    "criar seções transversais": part_cross_sections["cross sections"],

    "extrudar": part_extrude["extrude"],
    "extrusao": part_extrude["extrude"],
    "extrusão": part_extrude["extrude"],
    "extrudar objeto": part_extrude["extrude"],

    "arredondar": part_fillet["fillet"],
    "arredondamento": part_fillet["fillet"],
    "arredondar bordas": part_fillet["fillet"],
    "filete": part_fillet["fillet"],

    "loft": part_loft["loft"],
    "criar loft": part_loft["loft"],
    "fazer loft": part_loft["loft"],
    "unir perfis": part_loft["loft"],

    "criar face": part_makeface["makeface"],
    "fazer face": part_makeface["makeface"],
    "face": part_makeface["makeface"],

    "espelho": part_mirror["mirror"],
    "espelhar": part_mirror["mirror"],
    "refletir": part_mirror["mirror"],

    "deslocamento": part_offset["offset"],
    "offset": part_offset["offset"],
    "engrossar": part_offset["offset"],
    "encolher": part_offset["offset"],

    "offset 2d": part_offset2d["offset 2d"],
    "deslocamento 2d": part_offset2d["offset 2d"],
    "contorno": part_offset2d["offset 2d"],
    "borda": part_offset2d["offset 2d"],

    "projecao": part_projection_on_surface["projection"],
    "projeção": part_projection_on_surface["projection"],
    "projetar": part_projection_on_surface["projection"],
    "projetar na superficie": part_projection_on_surface["projection"],
    "projetar na superfície": part_projection_on_surface["projection"],
    "projetar desenho": part_projection_on_surface["projection"],

    "revolucao": part_revolve["revolve"],
    "revolução": part_revolve["revolve"],
    "revolucionar": part_revolve["revolve"],
    "criar revolucao": part_revolve["revolve"],
    "criar revolução": part_revolve["revolve"],

    "superficie regrada": part_ruled_surface["ruled surface"],
    "superfície regrada": part_ruled_surface["ruled surface"],
    "criar superficie regrada": part_ruled_surface["ruled surface"],
    "criar superfície regrada": part_ruled_surface["ruled surface"],
    "unir curvas": part_ruled_surface["ruled surface"],

    "escalar": part_scale["scale"],
    "escala": part_scale["scale"],
    "redimensionar": part_scale["scale"],
    "aumentar": part_scale["scale"],
    "reduzir": part_scale["scale"],

    "secao": part_section["section"],
    "seção": part_section["section"],
    "criar secao": part_section["section"],
    "criar seção": part_section["section"],
    "obter secao": part_section["section"],
    "obter seção": part_section["section"],
    "intersecao": part_section["section"],
    "interseção": part_section["section"],
    "curva de secao": part_section["section"],
    "curva de seção": part_section["section"],

    "varredura": part_sweep["sweep"],
    "varrer perfil": part_sweep["sweep"],
    "varrer caminho": part_sweep["sweep"],
    "varrer ao longo do caminho": part_sweep["sweep"],
    "sweep": part_sweep["sweep"],
    "tubo": part_sweep["sweep"],

    "ajuda": Part["help"],
    "informação": Part["help"],
    "opções": Part["help"]
,
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

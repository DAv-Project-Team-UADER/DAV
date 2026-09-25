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

"""Spanish spoken-word mapping for the DAV PartWorkbench dictionary."""

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

TraduceToEs = {
    "caja": box["box"],
    "crear caja": box["box"],
    "hacer caja": box["box"],

    "circulo": circle["circle"],
    "círculo": circle["circle"],
    "crear circulo": circle["circle"],
    "crear círculo": circle["circle"],

    "cono": cone["cone"],
    "crear cono": cone["cone"],
    "cono primitivo": cone["cone"],

    "cubo": cube["cube"],
    "crear cubo": cube["cube"],
    "hacer cubo": cube["cube"],

    "cilindro": cylinder["cylinder"],
    "crear cilindro": cylinder["cylinder"],
    "cilindro primitivo": cylinder["cylinder"],

    "elipse": ellipse["ellipse"],
    "crear elipse": ellipse["ellipse"],
    "hacer elipse": ellipse["ellipse"],

    "linea": line["line"],
    "línea": line["line"],
    "crear linea": line["line"],
    "crear línea": line["line"],

    "nuevo sketch": new_sketch["new sketch"],
    "nuevo boceto": new_sketch["new sketch"],
    "crear sketch": new_sketch["new sketch"],
    "crear boceto": new_sketch["new sketch"],

    "chaflan": part_chamfer["chaflan"],
    "chaflán": part_chamfer["chaflan"],
    "bisel": part_chamfer["chaflan"],
    "biselar": part_chamfer["chaflan"],

    "color por cara": part_color_per_face["paint face"],
    "pintar cara": part_color_per_face["paint face"],
    "colorear cara": part_color_per_face["paint face"],

    "secciones transversales": part_cross_sections["cross sections"],
    "cortes transversales": part_cross_sections["cross sections"],
    "crear secciones transversales": part_cross_sections["cross sections"],

    "extruir": part_extrude["extrude"],
    "extrusion": part_extrude["extrude"],
    "extrusión": part_extrude["extrude"],
    "extruir objeto": part_extrude["extrude"],

    "redondear": part_fillet["fillet"],
    "redondeo": part_fillet["fillet"],
    "redondear bordes": part_fillet["fillet"],
    "filete": part_fillet["fillet"],

    "loft": part_loft["loft"],
    "crear loft": part_loft["loft"],
    "hacer loft": part_loft["loft"],
    "unir perfiles": part_loft["loft"],

    "crear cara": part_makeface["makeface"],
    "hacer cara": part_makeface["makeface"],
    "cara": part_makeface["makeface"],

    "espejo": part_mirror["mirror"],
    "reflejar": part_mirror["mirror"],
    "simetria": part_mirror["mirror"],
    "simetría": part_mirror["mirror"],

    "desfase": part_offset["offset"],
    "offset": part_offset["offset"],
    "ensanchar": part_offset["offset"],
    "encoger": part_offset["offset"],

    "offset 2d": part_offset2d["offset 2d"],
    "desfase 2d": part_offset2d["offset 2d"],
    "contorno": part_offset2d["offset 2d"],
    "borde": part_offset2d["offset 2d"],

    "proyeccion": part_projection_on_surface["projection"],
    "proyección": part_projection_on_surface["projection"],
    "proyectar": part_projection_on_surface["projection"],
    "proyectar en superficie": part_projection_on_surface["projection"],
    "proyectar dibujo": part_projection_on_surface["projection"],

    "revolucion": part_revolve["revolve"],
    "revolución": part_revolve["revolve"],
    "revolucionar": part_revolve["revolve"],
    "crear revolucion": part_revolve["revolve"],
    "crear revolución": part_revolve["revolve"],

    "superficie reglada": part_ruled_surface["ruled surface"],
    "crear superficie reglada": part_ruled_surface["ruled surface"],
    "unir curvas": part_ruled_surface["ruled surface"],

    "escalar": part_scale["scale"],
    "escala": part_scale["scale"],
    "agrandar": part_scale["scale"],
    "reducir": part_scale["scale"],

    "seccion": part_section["section"],
    "sección": part_section["section"],
    "crear seccion": part_section["section"],
    "crear sección": part_section["section"],
    "obtener seccion": part_section["section"],
    "obtener sección": part_section["section"],
    "interseccion": part_section["section"],
    "intersección": part_section["section"],
    "curva de seccion": part_section["section"],
    "curva de sección": part_section["section"],
    "corte": part_section["section"],

    "barrido": part_sweep["sweep"],
    "barrer perfil": part_sweep["sweep"],
    "barrer trayectoria": part_sweep["sweep"],
    "barrer por trayectoria": part_sweep["sweep"],

    "ayuda": Part['help'],
    "información": Part['help'],
    "opciones": Part['help'],

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

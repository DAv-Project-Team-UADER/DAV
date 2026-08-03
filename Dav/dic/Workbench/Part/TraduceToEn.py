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

"""English spoken-word mapping for the DAV PartWorkbench dictionary."""

from DAV.FREECAD.src.App import Part

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

TraduceToEn = {
    "box": box["box"],
    "create box": box["box"],
    "make box": box["box"],

    "circle": circle["circle"],
    "create circle": circle["circle"],
    "make circle": circle["circle"],

    "cone": cone["cone"],
    "create cone": cone["cone"],
    "primitive cone": cone["cone"],

    "cube": cube["cube"],
    "create cube": cube["cube"],
    "make cube": cube["cube"],

    "cylinder": cylinder["cylinder"],
    "create cylinder": cylinder["cylinder"],
    "primitive cylinder": cylinder["cylinder"],

    "ellipse": ellipse["ellipse"],
    "create ellipse": ellipse["ellipse"],
    "make ellipse": ellipse["ellipse"],

    "line": line["line"],
    "create line": line["line"],
    "make line": line["line"],

    "new sketch": new_sketch["new sketch"],
    "create sketch": new_sketch["new sketch"],
    "new drawing": new_sketch["new sketch"],

    "chamfer": part_chamfer["chaflan"],
    "bevel": part_chamfer["chaflan"],
    "create chamfer": part_chamfer["chaflan"],

    "color per face": part_color_per_face["paint face"],
    "paint face": part_color_per_face["paint face"],
    "color face": part_color_per_face["paint face"],

    "cross sections": part_cross_sections["cross sections"],
    "create cross sections": part_cross_sections["cross sections"],
    "make cross sections": part_cross_sections["cross sections"],

    "extrude": part_extrude["extrude"],
    "create extrude": part_extrude["extrude"],
    "extrude object": part_extrude["extrude"],

    "fillet": part_fillet["fillet"],
    "round edges": part_fillet["fillet"],
    "round": part_fillet["fillet"],

    "loft": part_loft["loft"],
    "create loft": part_loft["loft"],
    "make loft": part_loft["loft"],
    "join profiles": part_loft["loft"],

    "make face": part_makeface["make face"],
    "create face": part_makeface["make face"],
    "face": part_makeface["make face"],

    "mirror": part_mirror["mirror"],
    "reflect": part_mirror["mirror"],
    "create mirror": part_mirror["mirror"],

    "offset": part_offset["offset"],
    "create offset": part_offset["offset"],
    "thicken": part_offset["offset"],
    "shrink": part_offset["offset"],

    "offset 2d": part_offset2d["offset 2d"],
    "2d offset": part_offset2d["offset 2d"],
    "outline": part_offset2d["offset 2d"],
    "border": part_offset2d["offset 2d"],

    "projection": part_projection_on_surface["projection"],
    "project": part_projection_on_surface["projection"],
    "project on surface": part_projection_on_surface["projection"],
    "project drawing": part_projection_on_surface["projection"],

    "revolve": part_revolve["revolve"],
    "create revolve": part_revolve["revolve"],
    "revolution": part_revolve["revolve"],

    "ruled surface": part_ruled_surface["ruled surface"],
    "create ruled surface": part_ruled_surface["ruled surface"],
    "join curves": part_ruled_surface["ruled surface"],

    "scale": part_scale["scale"],
    "resize": part_scale["scale"],
    "enlarge": part_scale["scale"],
    "reduce": part_scale["scale"],

    "section": part_section["section"],
    "create section": part_section["section"],
    "section curve": part_section["section"],
    "intersection": part_section["section"],

    "sweep": part_sweep["sweep"],
    "create sweep": part_sweep["sweep"],
    "sweep profile": part_sweep["sweep"],
    "sweep along path": part_sweep["sweep"],
    "pipe": part_sweep["sweep"],

    "help": Part['help'],
    "info": Part['help'],
    "options": Part['help'],
}


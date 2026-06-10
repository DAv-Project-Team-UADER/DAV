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

    "new sketch": new_sketch["new_sketch"],
    "create sketch": new_sketch["new_sketch"],
    "new drawing": new_sketch["new_sketch"],

    "chamfer": part_chamfer["part_chamfer"],
    "bevel": part_chamfer["part_chamfer"],
    "create chamfer": part_chamfer["part_chamfer"],

    "color per face": part_color_per_face["part_color_per_face"],
    "paint face": part_color_per_face["part_color_per_face"],
    "color face": part_color_per_face["part_color_per_face"],

    "cross sections": part_cross_sections["part_cross_sections"],
    "create cross sections": part_cross_sections["part_cross_sections"],
    "make cross sections": part_cross_sections["part_cross_sections"],

    "extrude": part_extrude["part_extrude"],
    "create extrude": part_extrude["part_extrude"],
    "extrude object": part_extrude["part_extrude"],

    "fillet": part_fillet["part_fillet"],
    "round edges": part_fillet["part_fillet"],
    "round": part_fillet["part_fillet"],

    "loft": part_loft["part_loft"],
    "create loft": part_loft["part_loft"],
    "make loft": part_loft["part_loft"],
    "join profiles": part_loft["part_loft"],

    "make face": part_makeface["part_makeface"],
    "create face": part_makeface["part_makeface"],
    "face": part_makeface["part_makeface"],

    "mirror": part_mirror["part_mirror"],
    "reflect": part_mirror["part_mirror"],
    "create mirror": part_mirror["part_mirror"],

    "offset": part_offset["part_offset"],
    "create offset": part_offset["part_offset"],
    "thicken": part_offset["part_offset"],
    "shrink": part_offset["part_offset"],

    "offset 2d": part_offset2d["part_offset2d"],
    "2d offset": part_offset2d["part_offset2d"],
    "outline": part_offset2d["part_offset2d"],
    "border": part_offset2d["part_offset2d"],

    "projection": part_projection_on_surface["part_projection_on_surface"],
    "project": part_projection_on_surface["part_projection_on_surface"],
    "project on surface": part_projection_on_surface["part_projection_on_surface"],
    "project drawing": part_projection_on_surface["part_projection_on_surface"],

    "revolve": part_revolve["part_revolve"],
    "create revolve": part_revolve["part_revolve"],
    "revolution": part_revolve["part_revolve"],

    "ruled surface": part_ruled_surface["part_ruled_surface"],
    "create ruled surface": part_ruled_surface["part_ruled_surface"],
    "join curves": part_ruled_surface["part_ruled_surface"],

    "scale": part_scale["part_scale"],
    "resize": part_scale["part_scale"],
    "enlarge": part_scale["part_scale"],
    "reduce": part_scale["part_scale"],

    "section": part_section["part_section"],
    "create section": part_section["part_section"],
    "section curve": part_section["part_section"],
    "intersection": part_section["part_section"],

    "sweep": part_sweep["part_sweep"],
    "create sweep": part_sweep["part_sweep"],
    "sweep profile": part_sweep["part_sweep"],
    "sweep along path": part_sweep["part_sweep"],
    "pipe": part_sweep["part_sweep"],

    "help": ayuda,
    "manual": ayuda,
    "support": ayuda,
    "documentation": ayuda,
}

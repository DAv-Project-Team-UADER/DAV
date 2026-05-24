# Copyright (C) 2026 El Equipo del Proyecto DAV
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

from .box.box         import box
from .circle.circle   import circle
from .cone.cone       import cone
from .cube.cube       import cube
from .cylinder.cylinder import cylinder
from .ellipse.ellipse import ellipse
from .line.line       import line
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

partWorkbench = {}
partWorkbench.update(box)
partWorkbench.update(circle)
partWorkbench.update(cone)
partWorkbench.update(cube)
partWorkbench.update(cylinder)
partWorkbench.update(ellipse)
partWorkbench.update(line)
partWorkbench.update(new_sketch)
partWorkbench.update(part_chamfer)
partWorkbench.update(part_color_per_face)
partWorkbench.update(part_cross_sections)
partWorkbench.update(part_extrude)
partWorkbench.update(part_fillet)
partWorkbench.update(part_loft)
partWorkbench.update(part_makeface)
partWorkbench.update(part_mirror)
partWorkbench.update(part_offset)
partWorkbench.update(part_offset2d)
partWorkbench.update(part_projection_on_surface)
partWorkbench.update(part_revolve)
partWorkbench.update(part_ruled_surface)
partWorkbench.update(part_scale)
partWorkbench.update(part_section)
partWorkbench.update(part_sweep)
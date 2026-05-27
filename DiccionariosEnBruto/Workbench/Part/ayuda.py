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

from .box.ayuda      import ayuda as ayuda_box
from .circle.ayuda   import ayuda as ayuda_circle
from .cone.ayuda     import ayuda as ayuda_cone
from .cube.ayuda     import ayuda as ayuda_cube
from .cylinder.ayuda import ayuda as ayuda_cylinder
from .ellipse.ayuda  import ayuda as ayuda_ellipse
from .line.ayuda     import ayuda as ayuda_line
from .new_sketch.ayuda import ayuda as ayuda_new_sketch
from .part_chamfer.ayuda import ayuda as ayuda_part_chamfer
from .part_color_per_face.ayuda import ayuda as ayuda_part_color_per_face
from .part_cross_sections.ayuda import ayuda as ayuda_part_cross_sections
from .part_extrude.ayuda import ayuda as ayuda_part_extrude
from .part_fillet.ayuda import ayuda as ayuda_part_fillet
from .part_loft.ayuda import ayuda as ayuda_part_loft
from .part_makeface.ayuda import ayuda as ayuda_part_makeface
from .part_mirror.ayuda import ayuda as ayuda_part_mirror
from .part_offset.ayuda import ayuda as ayuda_part_offset
from .part_offset2d.ayuda import ayuda as ayuda_part_offset2d
from .part_projection_on_surface.ayuda import ayuda as ayuda_part_projection_on_surface
from .part_revolve.ayuda import ayuda as ayuda_part_revolve
from .part_ruled_surface.ayuda import ayuda as ayuda_part_ruled_surface
from .part_scale.ayuda import ayuda as ayuda_part_scale
from .part_section.ayuda import ayuda as ayuda_part_section
from .part_sweep.ayuda import ayuda as ayuda_part_sweep

def ayuda():
    ayuda_box()
    print()
    ayuda_circle()
    print()
    ayuda_cone()
    print()
    ayuda_cube()
    print()
    ayuda_cylinder()
    print()
    ayuda_ellipse()
    print()
    ayuda_line()
    print()
    ayuda_new_sketch()
    print()
    ayuda_part_chamfer()
    print()
    ayuda_part_color_per_face()
    print()
    ayuda_part_cross_sections()
    print()
    ayuda_part_extrude()
    print()
    ayuda_part_fillet()
    print()
    ayuda_part_loft()
    print()
    ayuda_part_makeface()
    print()
    ayuda_part_mirror()
    print()
    ayuda_part_offset()
    print()
    ayuda_part_offset2d()
    print()
    ayuda_part_projection_on_surface()
    print()
    ayuda_part_revolve()
    print()
    ayuda_part_ruled_surface()
    print()
    ayuda_part_scale()
    print()
    ayuda_part_section()
    print()
    ayuda_part_sweep()

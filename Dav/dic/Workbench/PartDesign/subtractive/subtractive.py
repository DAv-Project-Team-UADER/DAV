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

import FreeCADGui as Gui
from .ayuda import ayuda
from ._parametric import (
    cut_box_by_size,
    cut_cone_by_size,
    cut_cylinder_by_size,
    cut_prism_by_size,
    cut_sphere_by_radius,
    cut_torus_by_size,
    groove_by_angle,
    blind_hole_by_size,
    groove_choose_sketch,
    hole_by_size,
    hole_choose_sketch,
    pocket_by_length,
    pocket_choose_sketch,
)

subtractive = {
    'pocket':               pocket_choose_sketch,
    'groove':               groove_choose_sketch,
    'hole':                 hole_choose_sketch,
    'subtractivebox':       cut_box_by_size,
    'subtractivecone':      cut_cone_by_size,
    'subtractivecylinder':  cut_cylinder_by_size,
    'subtractiveellipsoid': lambda: Gui.runCommand('PartDesign_SubtractiveEllipsoid', 0),
    'subtractivehelix':     lambda: Gui.runCommand('PartDesign_SubtractiveHelix', 0),
    'subtractiveloft':      lambda: Gui.runCommand('PartDesign_SubtractiveLoft', 0),
    'subtractivepipe':      lambda: Gui.runCommand('PartDesign_SubtractivePipe', 0),
    'subtractiveprism':     cut_prism_by_size,
    'subtractivesphere':    cut_sphere_by_radius,
    'subtractivetorus':     cut_torus_by_size,
    'subtractivewedge':     lambda: Gui.runCommand('PartDesign_SubtractiveWedge', 0),
    'pocket_by_length': pocket_by_length,
    'hole_by_size':     hole_by_size,
    'blind_hole':       blind_hole_by_size,
    'groove_by_angle':  groove_by_angle,
    'cut_box_by_size':      cut_box_by_size,
    'cut_cylinder_by_size': cut_cylinder_by_size,
    'cut_sphere_by_radius': cut_sphere_by_radius,
    'cut_cone_by_size':     cut_cone_by_size,
    'cut_torus_by_size':    cut_torus_by_size,
    'cut_prism_by_size':    cut_prism_by_size,
    'boolean':              lambda: Gui.runCommand('PartDesign_Boolean', 0),
    'help':                 ayuda,
}

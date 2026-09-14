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
from .joint.joint import joint
from .ayuda import ayuda
from ._parametric import (
    angle_joint,
    ball_joint,
    belt_joint,
    cylindrical_joint,
    distance_joint,
    fixed_joint,
    gears_joint,
    ground_part,
    parallel_joint,
    perpendicular_joint,
    rack_pinion_joint,
    revolute_joint,
    screw_joint,
    slider_joint,
)

# Subcontexto anidado: el Browser navega por niveles y espera
# assembly['joint'] como submenú (no aplanado), igual que Explorer/Explorer.py.
assembly = {}
assembly.update({'joint': joint})
assembly.update({
    'create':      lambda: Gui.runCommand('Assembly_CreateAssembly', 0),
    'newpart':     lambda: Gui.runCommand('Assembly_InsertNewPart', 0),
    'link':        lambda: Gui.runCommand('Assembly_InsertLink', 0),
    'solve':       lambda: Gui.runCommand('Assembly_SolveAssembly', 0),
    'view':        lambda: Gui.runCommand('Assembly_CreateView', 0),
    'simulation':  lambda: Gui.runCommand('Assembly_CreateSimulation', 0),
    'bom':         lambda: Gui.runCommand('Assembly_CreateBom', 0),
    'preferences': lambda: Gui.runCommand('Assembly_Preferences', 0),
    'grounded':    lambda: Gui.runCommand('Assembly_ToggleGrounded', 1),
    'fixed_joint':     fixed_joint,
    'revolute_joint':  revolute_joint,
    'slider_joint':    slider_joint,
    'distance_joint':  distance_joint,
    'angle_joint':     angle_joint,
    'ground_part':     ground_part,
    'ball_joint':          ball_joint,
    'cylindrical_joint':   cylindrical_joint,
    'parallel_joint':      parallel_joint,
    'perpendicular_joint': perpendicular_joint,
    'gears_joint':         gears_joint,
    'belt_joint':          belt_joint,
    'screw_joint':         screw_joint,
    'rack_pinion_joint':   rack_pinion_joint,
    'help':        ayuda,
})
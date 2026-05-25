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

joints = {
    'help': ayuda,
    'fixed': lambda: Gui.runCommand('Assembly_CreateJointFixed', 0),
    'revolute': lambda: Gui.runCommand('Assembly_CreateJointRevolute', 0),
    'cylindrical': lambda: Gui.runCommand('Assembly_CreateJointCylindrical', 0),
    'slider': lambda: Gui.runCommand('Assembly_CreateJointSlider', 0),
    'ball': lambda: Gui.runCommand('Assembly_CreateJointBall', 0),
    'distance': lambda: Gui.runCommand('Assembly_CreateJointDistance', 0),
    'parallel': lambda: Gui.runCommand('Assembly_CreateJointParallel', 0),
    'perpendicular': lambda: Gui.runCommand('Assembly_CreateJointPerpendicular', 0)
}

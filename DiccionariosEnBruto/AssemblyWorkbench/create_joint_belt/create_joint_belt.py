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


create_joint_belt = {
    'crear union de correa': lambda: Gui.runCommand('Assembly_CreateJointBelt', 0),
    'union de correa': lambda: Gui.runCommand('Assembly_CreateJointBelt', 0),
    'belt joint': lambda: Gui.runCommand('Assembly_CreateJointBelt', 0),
    'joint de correa': lambda: Gui.runCommand('Assembly_CreateJointBelt', 0),
    'transmision por correa': lambda: Gui.runCommand('Assembly_CreateJointBelt', 0),
    'correa de transmision': lambda: Gui.runCommand('Assembly_CreateJointBelt', 0),
    'cadena': lambda: Gui.runCommand('Assembly_CreateJointBelt', 0),
    'help': ayuda,
}

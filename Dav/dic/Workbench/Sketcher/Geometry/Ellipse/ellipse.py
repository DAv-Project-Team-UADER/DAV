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

ellipse = {
    'center':     lambda: Gui.runCommand('Sketcher_CreateEllipseByCenter', 0),
    '3points':    lambda: Gui.runCommand('Sketcher_CreateEllipseBy3Points', 0),
    'elliptic':   lambda: Gui.runCommand('Sketcher_CreateArcOfEllipse', 0),
    'hyperbolic': lambda: Gui.runCommand('Sketcher_CreateArcOfHyperbola', 0),
    'parabolic':  lambda: Gui.runCommand('Sketcher_CreateArcOfParabola', 0),
    'help':       ayuda,
}
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
from ._parametric import loft_profiles, pad_sketch

additive = {
    'pad':               lambda: Gui.runCommand('PartDesign_Pad', 0),
    'revolution':        lambda: Gui.runCommand('PartDesign_Revolution', 0),
    'additivehelix':     lambda: Gui.runCommand('PartDesign_AdditiveHelix', 0),
    'additiveloft':      lambda: Gui.runCommand('PartDesign_AdditiveLoft', 0),
    'additivepipe':      lambda: Gui.runCommand('PartDesign_AdditivePipe', 0),
    'additivebox':       lambda: Gui.runCommand('PartDesign_AdditiveBox', 0),
    'additivecone':      lambda: Gui.runCommand('PartDesign_AdditiveCone', 0),
    'additivecylinder':  lambda: Gui.runCommand('PartDesign_AdditiveCylinder', 0),
    'additiveellipsoid': lambda: Gui.runCommand('PartDesign_AdditiveEllipsoid', 0),
    'additiveprism':     lambda: Gui.runCommand('PartDesign_AdditivePrism', 0),
    'additivesphere':    lambda: Gui.runCommand('PartDesign_AdditiveSphere', 0),
    'additivetorus':     lambda: Gui.runCommand('PartDesign_AdditiveTorus', 0),
    'additivewedge':     lambda: Gui.runCommand('PartDesign_AdditiveWedge', 0),
    'pad_sketch':        pad_sketch,
    'loft_profiles':     loft_profiles,
    'help':              ayuda,
}

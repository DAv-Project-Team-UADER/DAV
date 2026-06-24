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

subtractive = {
    'pocket':               lambda: Gui.runCommand('PartDesign_Pocket', 0),
    'groove':               lambda: Gui.runCommand('PartDesign_Groove', 0),
    'hole':                 lambda: Gui.runCommand('PartDesign_Hole', 0),
    'subtractivebox':       lambda: Gui.runCommand('PartDesign_SubtractiveBox', 0),
    'subtractivecone':      lambda: Gui.runCommand('PartDesign_SubtractiveCone', 0),
    'subtractivecylinder':  lambda: Gui.runCommand('PartDesign_SubtractiveCylinder', 0),
    'subtractiveellipsoid': lambda: Gui.runCommand('PartDesign_SubtractiveEllipsoid', 0),
    'subtractivehelix':     lambda: Gui.runCommand('PartDesign_SubtractiveHelix', 0),
    'subtractiveloft':      lambda: Gui.runCommand('PartDesign_SubtractiveLoft', 0),
    'subtractivepipe':      lambda: Gui.runCommand('PartDesign_SubtractivePipe', 0),
    'subtractiveprism':     lambda: Gui.runCommand('PartDesign_SubtractivePrism', 0),
    'subtractivesphere':    lambda: Gui.runCommand('PartDesign_SubtractiveSphere', 0),
    'subtractivetorus':     lambda: Gui.runCommand('PartDesign_SubtractiveTorus', 0),
    'subtractivewedge':     lambda: Gui.runCommand('PartDesign_SubtractiveWedge', 0),
    'boolean':              lambda: Gui.runCommand('PartDesign_Boolean', 0),
    'help':                 ayuda,
}

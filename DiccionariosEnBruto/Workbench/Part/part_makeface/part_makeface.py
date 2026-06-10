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

import FreeCAD
import Part
import FreeCADGui as Gui
from .ayuda import ayuda


def _makeface():
    """Create a planar face from the selected closed wire."""
    sel = Gui.Selection.getSelection()
    if not sel:
        return
    doc = FreeCAD.activeDocument()
    shape = sel[0].Shape
    face = Part.makeFilledFace(shape.Wires)
    obj = doc.addObject("Part::Feature", "Face")
    obj.Shape = face
    sel[0].Visibility = False
    doc.recompute()


part_makeface = {
    'crear cara': _makeface,
    'make face': _makeface,
    'cara': _makeface,
    'help': ayuda,
}
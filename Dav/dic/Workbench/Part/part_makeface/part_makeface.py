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
    if not doc:
        return
    obj_sel = sel[0]
    if not hasattr(obj_sel, "Shape") or not obj_sel.Shape.Wires:
        return
    face = Part.makeFilledFace(obj_sel.Shape.Wires)
    obj = doc.addObject("Part::Feature", "Face")
    obj.Shape = face
    if hasattr(obj_sel, "Visibility"):
        obj_sel.Visibility = False
    doc.recompute()


part_makeface = {
    'makeface': _makeface,
    'createface': _makeface,
    'upgrade': lambda: Gui.runCommand('Draft_Upgrade', 0),
    'help': ayuda,
}
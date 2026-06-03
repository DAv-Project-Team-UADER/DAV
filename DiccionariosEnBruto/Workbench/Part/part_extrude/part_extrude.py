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
from FreeCAD import Vector
import FreeCADGui as Gui
from .ayuda import ayuda


def _extrude():
    """Extrude the selected Part object 10 mm along the Z axis."""
    sel = Gui.Selection.getSelection()
    if not sel:
        return
    doc = FreeCAD.activeDocument()
    f = doc.addObject("Part::Extrusion", "Extrude")
    f.Base = sel[0]
    f.Dir = Vector(0, 0, 10)
    f.Solid = True
    sel[0].Visibility = False
    doc.recompute()


part_extrude = {
    'extruir': _extrude,
    'extrude': _extrude,
    'extruir objeto': _extrude,
    'help': ayuda,
}
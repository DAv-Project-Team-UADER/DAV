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


def _revolve():
    """Revolve the selected Part object 360 degrees around the Z axis."""
    sel = Gui.Selection.getSelection()
    if not sel:
        return
    doc = FreeCAD.activeDocument()
    f = doc.addObject("Part::Revolution", "Revolve")
    f.Source = sel[0]
    f.Axis = Vector(0, 0, 1)
    f.Base = Vector(0, 0, 0)
    f.Angle = 360.0
    f.Solid = True
    sel[0].Visibility = False
    doc.recompute()
    try:
        from createobjects import CreateObjects
    except ImportError:
        from selection.createobjects import CreateObjects
    CreateObjects(f.Name, Is3D=True).Execute()


part_revolve = {
    'revolucion': _revolve,
    'revolución': _revolve,
    'revolve': _revolve,
    'help': ayuda,
}
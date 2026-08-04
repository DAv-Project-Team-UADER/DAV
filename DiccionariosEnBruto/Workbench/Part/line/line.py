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

import FreeCAD as App
from .ayuda import ayuda
try:
    from createobjects import CreateObjects
except ImportError:
    from selection.createobjects import CreateObjects


def _create_line(x1: float, y1: float, z1: float, x2: float, y2: float, z2: float):
    doc = App.activeDocument()
    if doc is None:
        doc = App.newDocument()
    line = doc.addObject("Part::Line", "Line")
    line.X1 = x1
    line.Y1 = y1
    line.Z1 = z1
    line.X2 = x2
    line.Y2 = y2
    line.Z2 = z2
    doc.recompute()
    CreateObjects(line.Name, Is3D=False).Execute()


line = {
    'line': _create_line,
    'help':  ayuda,
}
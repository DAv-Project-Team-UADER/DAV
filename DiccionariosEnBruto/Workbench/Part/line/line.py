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


def _create_line(x1=0, y1=0, z1=0, x2=10, y2=10, z2=0):
    doc = App.activeDocument()
    line = doc.addObject("Part::Line", "Line")
    line.X1 = x1
    line.Y1 = y1
    line.Z1 = z1
    line.X2 = x2
    line.Y2 = y2
    line.Z2 = z2
    doc.recompute()


line = {
    'line': lambda: _create_line(),
    'help':  ayuda,
}
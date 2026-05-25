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

def _create_wedge(xmin=0, ymin=0, zmin=0, x2min=2, z2min=2, xmax=10, ymax=15, zmax=10, x2max=8, z2max=8):
    doc = App.activeDocument()
    wedge = doc.addObject("Part::Wedge", "Wedge")
    wedge.Xmin = xmin
    wedge.Ymin = ymin
    wedge.Zmin = zmin
    wedge.X2min = x2min
    wedge.Z2min = z2min
    wedge.Xmax = xmax
    wedge.Ymax = ymax
    wedge.Zmax = zmax
    wedge.X2max = x2max
    wedge.Z2max = z2max
    doc.recompute()

wedge = {
    'cuna': lambda: _create_wedge(),
    'primitive wedge': lambda: _create_wedge(),
    'help': ayuda,
}

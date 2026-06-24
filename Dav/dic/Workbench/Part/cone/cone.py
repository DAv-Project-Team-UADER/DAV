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
 
 
def _create_cone(radius1=2, radius2=4, height=10, angle=360):
    doc = App.activeDocument()
    cone = doc.addObject("Part::Cone", "Cone")
    cone.Radius1 = radius1
    cone.Radius2 = radius2
    cone.Height  = height
    cone.Angle   = angle
    doc.recompute()
 
 
cone = {
    'cone':           lambda: _create_cone(),
    'primitive cone': lambda: _create_cone(),
    'help':           ayuda,
}
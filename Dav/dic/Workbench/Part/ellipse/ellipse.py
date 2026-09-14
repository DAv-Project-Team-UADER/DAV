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


def _create_ellipse(major_radius=4, minor_radius=2, angle1=0, angle2=360):
    doc = App.activeDocument()
    ellipse = doc.addObject("Part::Ellipse", "Ellipse")
    ellipse.MajorRadius = major_radius
    ellipse.MinorRadius = minor_radius
    ellipse.Angle1      = angle1
    ellipse.Angle2      = angle2
    doc.recompute()
    try:
        from createobjects import CreateObjects
    except ImportError:
        from selection.createobjects import CreateObjects
    CreateObjects(ellipse.Name, Is3D=False).Execute()


ellipse = {
    'ellipse': lambda: _create_ellipse(),
    'help':   ayuda,
}
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


def _create_box(length=10, width=10, height=10):
    doc = App.activeDocument()
    box = doc.addObject("Part::Box", "Box")
    box.Length = length
    box.Width  = width
    box.Height = height
    doc.recompute()
    CreateObjects(box.Name, Is3D=True).Execute()


box = {
    'box': lambda: _create_box(),
    'help': ayuda,
}
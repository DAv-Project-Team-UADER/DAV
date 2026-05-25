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


def _create_helix(pitch=1.0, height=2.0, radius=1.0, angle=0.0):
    doc = App.activeDocument()
    helix = doc.addObject("Part::Helix", "Helix")
    helix.Pitch = pitch
    helix.Height = height
    helix.Radius = radius
    helix.Angle = angle
    doc.recompute()


helix = {
    'helice': lambda: _create_helix(),
    'primitive helix': lambda: _create_helix(),
    'help': ayuda,
}

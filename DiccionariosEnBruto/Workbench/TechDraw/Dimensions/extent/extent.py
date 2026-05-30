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
import TechDraw
from .ayuda import ayuda


def _create_extent(view_name="View", edge1="Edge1", edge2="Edge2"):
    doc  = App.activeDocument()
    view = doc.getObject(view_name)
    selection = [edge1, edge2]
    TechDraw.makeExtentDim(view, selection, 0)
    doc.DimExtent.Y         = -60
    doc.DimExtent.X         = 10
    doc.DimExtent.FormatSpec = "%.0f"
    doc.recompute()


extent = {
    'extent': lambda: _create_extent(),
    'help':   ayuda,
}

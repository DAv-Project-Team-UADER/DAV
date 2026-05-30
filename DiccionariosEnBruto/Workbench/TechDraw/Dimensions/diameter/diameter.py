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


def _create_diameter(page_name="Page", view_name="View", edge="Edge1"):
    doc  = App.activeDocument()
    page = doc.getObject(page_name)
    view = doc.getObject(view_name)
    dim  = doc.addObject("TechDraw::DrawDimDiameter", "DiameterDimension")
    dim.Source       = view
    dim.References2D = [(view, edge)]
    dim.Page         = page
    page.addView(dim)
    doc.recompute()


diameter = {
    'diameter': lambda: _create_diameter(),
    'help':     ayuda,
}

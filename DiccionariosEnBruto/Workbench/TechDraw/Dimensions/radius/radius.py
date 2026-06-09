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

# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
# Este programa es software libre: usted puede redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU tal como fue publicada
# por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#
# Este programa se distribuibe con la esperanza de que sea útil,
# pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
# MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
# Licencia Pública General GNU para más detalles.
#
# Deberías haber recibido una copia de la Licencia Pública General GNU
# junto con este programa. Si no es así, consulte <http://www.gnu.org/licenses/>.

import FreeCAD as App
import FreeCADGui as Gui
from .ayuda import ayuda


def _create_radius():
    """Add a radius dimension to the active TechDraw page using the current selection.

    The user must pre-select one circular edge in a TechDraw view.
    """
    sel = Gui.Selection.getSelectionEx()
    if not sel:
        print("Seleccioná una arista circular en la vista TechDraw primero.")
        return
    doc  = App.activeDocument()
    view = sel[0].Object
    edge = sel[0].SubElementNames[0] if sel[0].SubElementNames else "Edge1"
    page = next((o for o in doc.Objects if o.isDerivedFrom("TechDraw::DrawPage")), None)
    if page is None:
        print("No se encontró ninguna página TechDraw en el documento.")
        return
    dim              = doc.addObject("TechDraw::DrawViewDimension", "RadiusDimension")
    dim.Type         = "Radius"
    dim.References2D = [(view, edge)]
    page.addView(dim)
    doc.recompute()


radius = {
    'radius': lambda: _create_radius(),
    'help':   ayuda,
}

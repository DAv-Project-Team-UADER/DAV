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
import FreeCADGui as Gui
from .ayuda import ayuda


def _selectedEdge(selEx):
    """Return the first selected edge sub-element name, if any.

    Args:
        selEx: FreeCAD selection entry from Gui.Selection.getSelectionEx().

    Returns:
        str | None: Edge name such as ``Edge1``, or None when missing.
    """
    for name in selEx.SubElementNames:
        if name.startswith("Edge"):
            return name
    return None


def _create_length():
    """Add a length dimension to the active TechDraw page using the current selection.

    The user must pre-select one edge in a TechDraw view before invoking this command.

    Example::
        _create_length()
    """
    sel = Gui.Selection.getSelectionEx()
    if not sel:
        print("Seleccioná una arista en la vista TechDraw primero.")
        return

    view = sel[0].Object
    if view is None or not view.isDerivedFrom("TechDraw::DrawView"):
        print("La selección debe ser una arista dentro de una vista TechDraw.")
        return

    edge = _selectedEdge(sel[0])
    if edge is None:
        print(
            "Seleccioná una arista en el plano (pestaña Page, click en la línea "
            "del dibujo). Debe verse View : Edge… en la barra de estado."
        )
        return

    doc = App.activeDocument()
    if doc is None:
        print("No hay documento activo.")
        return

    page = getattr(view, "Page", None)
    if page is None:
        page = next(
            (obj for obj in doc.Objects if obj.isDerivedFrom("TechDraw::DrawPage")),
            None,
        )
    if page is None:
        print("No se encontró ninguna página TechDraw en el documento.")
        return

    dim = doc.addObject("TechDraw::DrawViewDimension", "LengthDimension")
    dim.Type = "Distance"
    dim.References2D = [(view, edge)]
    page.addView(dim)
    doc.recompute()


length = {
    'length': lambda: _create_length(),
    'help':   ayuda,
}

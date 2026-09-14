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
try:
    import TechDraw
except ImportError as _e:
    TechDraw = None  # type: ignore
    print(f"[DAV] TechDraw no disponible ({_e}); 'extent' queda como no-op.")
from .ayuda import ayuda


def _create_extent():
    """Add an extent dimension to the active TechDraw page using the current selection.

    The user must pre-select two edges in a TechDraw view.
    """
    if TechDraw is None:
        print("TechDraw no disponible en este sistema; no se puede crear cota de extensión.")
        return
    sel = Gui.Selection.getSelectionEx()
    if not sel or len(sel[0].SubElementNames) < 2:
        print("Seleccioná dos aristas en la vista TechDraw primero.")
        return
    doc   = App.activeDocument()
    view  = sel[0].Object
    edges = list(sel[0].SubElementNames[:2])
    TechDraw.makeExtentDim(view, edges, 0)
    doc.recompute()


extent = {
    'extent': lambda: _create_extent(),
    'help':   ayuda,
}

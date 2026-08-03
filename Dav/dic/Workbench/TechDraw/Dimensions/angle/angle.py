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


def _create_angle():
    """Add an angle dimension to the active TechDraw page using the current selection.

    The user must pre-select two edges in a TechDraw view.
    """
    sel = Gui.Selection.getSelectionEx()
    if not sel or len(sel[0].SubElementNames) < 2:
        print("Seleccioná dos aristas en la vista TechDraw primero.")
        return
    doc  = App.activeDocument()
    view = sel[0].Object
    refs = [(view, name) for name in sel[0].SubElementNames[:2]]
    page = next((o for o in doc.Objects if o.isDerivedFrom("TechDraw::DrawPage")), None)
    if page is None:
        print("No se encontró ninguna página TechDraw en el documento.")
        return
    dim              = doc.addObject("TechDraw::DrawViewDimension", "AngleDimension")
    dim.Type         = "Angle"
    dim.References2D = refs
    page.addView(dim)
    doc.recompute()


def _create_angle_3pt():
    """Add a 3-point angle dimension to the active TechDraw page using the current selection.

    The user must pre-select three vertices in a TechDraw view.
    """
    sel = Gui.Selection.getSelectionEx()
    if not sel or len(sel[0].SubElementNames) < 3:
        print("Seleccioná tres vértices en la vista TechDraw primero.")
        return
    doc  = App.activeDocument()
    view = sel[0].Object
    refs = [(view, name) for name in sel[0].SubElementNames[:3]]
    page = next((o for o in doc.Objects if o.isDerivedFrom("TechDraw::DrawPage")), None)
    if page is None:
        print("No se encontró ninguna página TechDraw en el documento.")
        return
    dim              = doc.addObject("TechDraw::DrawViewDimension", "AngleDimension3Pt")
    dim.Type         = "Angle3Pt"
    dim.References2D = refs
    page.addView(dim)
    doc.recompute()


angle = {
    'angle':  lambda: _create_angle(),
    'points': lambda: _create_angle_3pt(),
    'help':   ayuda,
}

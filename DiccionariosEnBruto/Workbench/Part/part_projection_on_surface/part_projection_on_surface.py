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

import FreeCAD
import FreeCADGui as Gui
from .ayuda import ayuda


def _projection_on_surface():
    """Project the selected shape onto a target surface via the Part API."""
    sel = Gui.Selection.getSelection()
    if len(sel) < 2:
        return
    doc = FreeCAD.activeDocument()
    f = doc.addObject("Part::ProjectionOnSurface", "ProjectionOnSurface")
    f.SupportObject = sel[0]
    for obj in sel[1:]:
        f.addProjectedObject(obj, "All")
    sel[0].Visibility = False
    doc.recompute()


part_projection_on_surface = {
    'proyectar dibujo': _projection_on_surface,
    'proyectar': _projection_on_surface,
    'projection': _projection_on_surface,
    'help': ayuda,
}
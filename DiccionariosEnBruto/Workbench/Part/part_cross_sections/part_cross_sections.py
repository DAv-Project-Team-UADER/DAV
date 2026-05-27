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


def _cross_sections():
    doc = App.activeDocument()

    sel = App.Gui.Selection.getSelection() if hasattr(App, "Gui") else []
    if not sel:
        return

    base = sel[0]

    obj = doc.addObject("Part::Compound", "CrossSections")
    obj.Label = "Cross Sections"

    doc.recompute()


part_cross_sections = {
    'secciones transversales': lambda: _cross_sections(),
    'cross sections': lambda: _cross_sections(),
    'help': ayuda,
}
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
# SPDX-License-Identifier: GPL-3.0-or-later

import FreeCAD as App

from selection.objectselection import ObjectSelection
from .ayuda import ayuda

SelectorInstance = ObjectSelection()


def SelectNext():
    """Selects the next object from the active document."""

    ActiveDoc = App.activeDocument()

    if not ActiveDoc:
        print("Error: There is no active document in FreeCAD.")
        return

    if not SelectorInstance._ObjectNames:
        ObjectNames = [Obj.Name for Obj in ActiveDoc.Objects]
        SelectorInstance.VectorSelection(ObjectNames)

    SelectorInstance.SelectNext()


selection = {
    'next': SelectNext,
    'help': ayuda
}

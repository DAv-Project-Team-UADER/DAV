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

"""Helpers shared by the guided examples."""

import FreeCAD as App


def activeDoc():
    """Return the active document, creating one when there is none."""
    doc = App.ActiveDocument
    if doc is None:
        doc = App.newDocument("Ejemplo")
    return doc


def fitView() -> None:
    """Fit the 3D view to the model. Does nothing without a GUI."""
    try:
        import FreeCADGui as Gui

        if Gui.ActiveDocument is not None and Gui.ActiveDocument.ActiveView is not None:
            Gui.SendMsgToActiveView("ViewFit")
    except Exception:
        pass


def lastOfType(doc, typeId: str):
    """Return the most recent object of ``typeId``, or raise if there is none."""
    found = [obj for obj in doc.Objects if obj.TypeId == typeId]
    if not found:
        raise RuntimeError(f"Falta un objeto {typeId}: seguí los cuadros en orden.")
    return found[-1]

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
import FreeCADGui as Gui

from .ayuda import ayuda
from ._parametric import create_by_vertices
from selection.createobjects import CreateObjects


def _execute_with_objects(command):
    Gui.runCommand(command, 0)
    active_doc = App.ActiveDocument
    if active_doc and getattr(active_doc, 'ActiveObject', None):
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def create_by_vertices_with_objects(
    x1: float, y1: float, x2: float, y2: float, x3: float, y3: float, label: str = "Triangle"
):
    create_by_vertices(x1=x1, y1=y1, x2=x2, y2=y2, x3=x3, y3=y3, label=label)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


triangle = {
    # 'create' es paramétrico con ventana (igual que circle.create): cada float
    # dispara un InputPrompt via ParameterCollector, no la herramienta del mouse.
    'create': create_by_vertices_with_objects,
    'create_by_vertices': create_by_vertices_with_objects,
    # modo interactivo legacy por si se necesita mouse (no usado por voz pura)
    'interactive': lambda: _execute_with_objects('Sketcher_CreateTriangle'),
    'help':   ayuda
}

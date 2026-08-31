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
from ._parametric import create_by_center
from selection.createobjects import CreateObjects


def _execute_with_objects(command):
    Gui.runCommand(command, 0)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def create_by_center_with_objects(x: float, y: float, major_radius: float, minor_radius: float, label: str = "Ellipse"):
    create_by_center(x=x, y=y, major_radius=major_radius, minor_radius=minor_radius, label=label)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


ellipse = {
    'center':           lambda: _execute_with_objects('Sketcher_CreateEllipseByCenter'),
    '3points':          lambda: _execute_with_objects('Sketcher_CreateEllipseBy3Points'),
    'elliptic':         lambda: _execute_with_objects('Sketcher_CreateArcOfEllipse'),
    'hyperbolic':       lambda: _execute_with_objects('Sketcher_CreateArcOfHyperbola'),
    'parabolic':        lambda: _execute_with_objects('Sketcher_CreateArcOfParabola'),
    'create_by_center': create_by_center_with_objects,
    'help':             ayuda,
}

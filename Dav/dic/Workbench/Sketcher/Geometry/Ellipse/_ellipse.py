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
from ._parametric import (
    create_by_center,
    create_by_3_points,
    create_elliptic_arc,
    create_hyperbolic_arc,
    create_parabolic_arc,
)
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


def create_by_3_points_with_objects(x1: float, y1: float, x2: float, y2: float, x3: float, y3: float, label: str = "Ellipse3P"):
    create_by_3_points(x1=x1, y1=y1, x2=x2, y2=y2, x3=x3, y3=y3, label=label)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def create_elliptic_arc_with_objects(x: float, y: float, major_radius: float, minor_radius: float, angle1: float, angle2: float, label: str = "ArcEllipse"):
    create_elliptic_arc(x=x, y=y, major_radius=major_radius, minor_radius=minor_radius, angle1=angle1, angle2=angle2, label=label)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def create_hyperbolic_arc_with_objects(x: float, y: float, major_radius: float, minor_radius: float, angle1: float, angle2: float, label: str = "ArcHyperbola"):
    create_hyperbolic_arc(x=x, y=y, major_radius=major_radius, minor_radius=minor_radius, angle1=angle1, angle2=angle2, label=label)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def create_parabolic_arc_with_objects(x_focus: float, y_focus: float, x_vertex: float, y_vertex: float, angle1: float, angle2: float, label: str = "ArcParabola"):
    create_parabolic_arc(x_focus=x_focus, y_focus=y_focus, x_vertex=x_vertex, y_vertex=y_vertex, angle1=angle1, angle2=angle2, label=label)
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


ellipse = {
    # paramétricos con ventana (como line/circle) — cada float abre InputPrompt
    'center':     create_by_center_with_objects,
    '3points':    create_by_3_points_with_objects,
    'elliptic':   create_elliptic_arc_with_objects,
    'hyperbolic': create_hyperbolic_arc_with_objects,
    'parabolic':  create_parabolic_arc_with_objects,
    # alias explícitos (voz: 'elipse por ...')
    'create_by_center':   create_by_center_with_objects,
    'create_by_3_points': create_by_3_points_with_objects,
    'create_elliptic':    create_elliptic_arc_with_objects,
    'create_hyperbolic':  create_hyperbolic_arc_with_objects,
    'create_parabolic':   create_parabolic_arc_with_objects,
    # modo interactivo legacy (mouse dentro de sketch)
    'interactive_center':     lambda: _execute_with_objects('Sketcher_CreateEllipseByCenter'),
    'interactive_3points':    lambda: _execute_with_objects('Sketcher_CreateEllipseBy3Points'),
    'interactive_elliptic':   lambda: _execute_with_objects('Sketcher_CreateArcOfEllipse'),
    'interactive_hyperbolic': lambda: _execute_with_objects('Sketcher_CreateArcOfHyperbola'),
    'interactive_parabolic':  lambda: _execute_with_objects('Sketcher_CreateArcOfParabola'),
    'help':             ayuda,
}

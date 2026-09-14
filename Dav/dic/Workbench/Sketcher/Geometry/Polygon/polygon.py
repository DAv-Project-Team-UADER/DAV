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
from .ayuda import ayuda
from ._parametric import create_regular
from selection.createobjects import CreateObjects


def _register_active_object():
    active_doc = App.ActiveDocument
    if active_doc and active_doc.ActiveObject:
        CreateObjects(ObjectName=active_doc.ActiveObject.Name, Is3D=False).Execute()


def create_regular_with_objects(sides: int, x: float, y: float, radius: float, label: str = "Polygon"):
    create_regular(sides=sides, x=x, y=y, radius=radius, label=label)
    _register_active_object()


def create_pentagon_with_objects(x: float, y: float, radius: float, label: str = "Pentagon"):
    create_regular(sides=5, x=x, y=y, radius=radius, label=label)
    _register_active_object()


def create_octagon_with_objects(x: float, y: float, radius: float, label: str = "Octagon"):
    create_regular(sides=8, x=x, y=y, radius=radius, label=label)
    _register_active_object()


# 'create_regular_polygon' se mantiene como alias de la clave histórica que usa
# TraduceTo*.py (polígono por parámetros), apuntando al mismo flujo por voz.
polygon = {
    'pentagon': create_pentagon_with_objects,
    'octagon':  create_octagon_with_objects,
    'regular':  create_regular_with_objects,
    'create_regular': create_regular_with_objects,
    'create_regular_polygon': create_regular_with_objects,
    'help':    ayuda,
}
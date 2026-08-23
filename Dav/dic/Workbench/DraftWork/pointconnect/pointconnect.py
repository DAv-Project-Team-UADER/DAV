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
import Draft
import Part
from .ayuda import ayuda

def _get_selected_points():
    """Gets the points from the selected objects."""
    sel = App.Gui.Selection.getSelection()
    if not sel:
        return []
    
    points = []
    for obj in sel:
        if hasattr(obj, 'Shape') and obj.Shape.Vertexes:
            points.append(obj.Shape.Vertexes[0].Point)
    return points

def _connect():
    points = _get_selected_points()
    if len(points) >= 2:
        Draft.make_wire(points, closed=False)
        App.ActiveDocument.recompute()

def _createline():
    points = _get_selected_points()
    if len(points) >= 2:
        linea = App.ActiveDocument.addObject("Part::Feature", "Line")
        linea.Shape = Part.makeLine(points[0], points[1])
        App.ActiveDocument.recompute()

def _closewire():
    points = _get_selected_points()
    if len(points) >= 2:
        Draft.make_wire(points, closed=True)
        App.ActiveDocument.recompute()

def _createpolygon():
    points = _get_selected_points()
    if len(points) >= 3:
        Draft.make_wire(points, closed=True)
        App.ActiveDocument.recompute()

pointconnect = {
    'connect': _connect,
    'createline': _createline,
    'closewire': _closewire,
    'createpolygon': _createpolygon,
    'help': ayuda
}
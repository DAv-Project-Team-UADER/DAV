#  Copyright (C) 2026 The DAV Project Team
#  Copyright (C) 2026 El Equipo del Proyecto DAV
#  Universidad Autónoma de Entre Ríos (UADER)
#  Directed by Gerard Guillermo and Gallo Fabricio David
#  Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, in GPLv3 version of the License
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <https://www.gnu.org/licenses/>.
#  SPDX-License-Identifier: GPL-3.0-or-later

import FreeCAD as App
import FreeCADGui as Gui
import Draft


def CreateDimension(x1: int, y1: int, z1: int, x2: int, y2: int, z2: int):
    """
    Creates a linear dimension between Point1(x1, y1, z1) and Point2(x2, y2, z2).
    Coordinates are integer parameters collected via DAV voice prompts.
    """
    active_doc = App.ActiveDocument
    if active_doc is None:
        active_doc = App.newDocument()

    point1 = App.Vector(float(x1), float(y1), float(z1))
    point2 = App.Vector(float(x2), float(y2), float(z2))

    line_vector = point2.sub(point1)
    if line_vector.Length == 0:
        App.Console.PrintError("Error: Point 1 and Point 2 coincide.\n")
        return None

    # Calculate normal vector for dimension offset line
    normal_vector = App.Vector(-line_vector.y, line_vector.x, 0.0)
    if normal_vector.Length == 0:
        normal_vector = App.Vector(0.0, 0.0, 1.0)
    normal_vector.normalize()

    offset_distance = 10.0
    dimension_point = point1.add(normal_vector.multiply(offset_distance))

    active_doc.openTransaction("Create Dimension")
    dim_obj = Draft.make_dimension(point1, point2, dimension_point)
    active_doc.commitTransaction()
    active_doc.recompute()
    App.Console.PrintMessage(f"Dimension successfully created between {point1} and {point2}.\n")
    return dim_obj

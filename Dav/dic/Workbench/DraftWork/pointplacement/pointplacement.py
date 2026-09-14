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
import Draft
from .ayuda import ayuda


def addpoint():
    """Places a point at the current selected vertex or the first vertex of the selected object."""
    sel_ex = Gui.Selection.getSelectionEx()
    if not sel_ex:
        print("Error: No object is selected.")
        return
    
    sub_objs = sel_ex[0].SubObjects
    sub_names = sel_ex[0].SubElementNames
    
    found_vertex = None
    for name, sub in zip(sub_names, sub_objs):
        if "Vertex" in name:
            found_vertex = sub
            break
            
    if found_vertex:
        x, y, z = found_vertex.X, found_vertex.Y, found_vertex.Z
    else:
        obj = sel_ex[0].Object
        if hasattr(obj, "Shape") and obj.Shape.Vertexes:
            v = obj.Shape.Vertexes[0]
            x, y, z = v.X, v.Y, v.Z
        else:
            print("Error: The selected object has no vertices.")
            return

    Draft.make_point(x, y, z)
    App.ActiveDocument.recompute()
    print(f"Point placed at vertex: {x}, {y}, {z}")


def pointatvertex(index: int):
    """Places a point at a specific vertex index of the selected object."""
    sel_ex = Gui.Selection.getSelectionEx()
    if not sel_ex:
        print("Error: No object is selected.")
        return
    
    obj = sel_ex[0].Object
    if not hasattr(obj, "Shape") or not obj.Shape.Vertexes:
        print("Error: The selected object has no vertices.")
        return
        
    vertexes = obj.Shape.Vertexes
    if index < 0 or index >= len(vertexes):
        print(f"Error: Vertex index {index} is out of range (0-{len(vertexes) - 1}).")
        return
        
    vertex = vertexes[index]
    Draft.make_point(vertex.X, vertex.Y, vertex.Z)
    App.ActiveDocument.recompute()
    print(f"Point placed at vertex {index}: {vertex.X}, {vertex.Y}, {vertex.Z}")


def midpoint(edge_index: int = 0):
    """Places a point at the midpoint of the selected edge subelement or the specified edge index."""
    sel_ex = Gui.Selection.getSelectionEx()
    if not sel_ex:
        print("Error: No object is selected.")
        return
        
    sub_objs = sel_ex[0].SubObjects
    sub_names = sel_ex[0].SubElementNames
    
    found_edge = None
    for name, sub in zip(sub_names, sub_objs):
        if "Edge" in name:
            found_edge = sub
            break
            
    if not found_edge:
        obj = sel_ex[0].Object
        if hasattr(obj, "Shape") and obj.Shape.Edges:
            if edge_index < 0 or edge_index >= len(obj.Shape.Edges):
                print(f"Error: Edge index {edge_index} is out of range (0-{len(obj.Shape.Edges) - 1}).")
                return
            found_edge = obj.Shape.Edges[edge_index]
        else:
            print("Error: The selected object has no edges.")
            return

    if len(found_edge.Vertexes) >= 2:
        v1 = found_edge.Vertexes[0]
        v2 = found_edge.Vertexes[-1]
        x = (v1.X + v2.X) / 2.0
        y = (v1.Y + v2.Y) / 2.0
        z = (v1.Z + v2.Z) / 2.0
        Draft.make_point(x, y, z)
        App.ActiveDocument.recompute()
        print(f"Point placed at midpoint: {x}, {y}, {z}")
    else:
        print("Error: The selected edge has fewer than 2 vertices.")


def pointatcoords(x: float, y: float, z: float):
    """Places a point at absolute X, Y, Z coordinates."""
    Draft.make_point(x, y, z)
    App.ActiveDocument.recompute()
    print(f"Point placed at coordinates: {x}, {y}, {z}")


pointplacement = {
    "addpoint": addpoint,
    "pointatvertex": pointatvertex,
    "midpoint": midpoint,
    "pointatcoords": pointatcoords,
    "help": ayuda,
}

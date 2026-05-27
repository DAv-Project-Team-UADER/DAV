#  Copyright (C) 2026 The DAV Project Team-                                 |#  Copyright (C) 2026 El Equipo del Proyecto DAV
#  Universidad Autónoma de Entre Ríos (UADER)                               |#  Universidad Autónoma de Entre Ríos (UADER)
#  Directed by Gerard Guillermo and Gallo Fabricio David                    |#  Bajo la dirección de Guillermo Gerard y Gallo Fabricio David
#                                                                           |#
#  This program is free software: you can redistribute it and/or modify     |#  Este programa es software libre: usted puede redistribuirlo y/o modificarlo
#  it under the terms of the GNU General Public License as published by     |#  bajo los términos de la Licencia Pública General GNU tal como fue publicada 
#  the Free Software Foundation, in GLPv3 version  of the License           |#  por la Fundación para el Software Libre, en la versión 3 de la Licencia.
#                                                                           |#
#  This program is distributed in the hope that it will be useful,          |#  Este programa se distribuye con la esperanza de que sea útil,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of           |#  pero SIN NINGUNA GARANTÍA; incluso sin la garantía implícita de
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the            |#  MERCANTIBILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Consulte la
#  GNU General Public License for more details.                             |#  Licencia Pública General GNU para más detalles.
#                                                                           |#
#  You should have received a copy of the GNU General Public License        |#  Deberías haber recibido una copia de la Licencia Pública General GNU
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.   |#  junto con este programa. Si no es así, consulte <https://www.gnu.org/licenses/>.

import FreeCAD as App
import Part

class CreateObjects:
    def __init__(self, ObjectName, Is3D=False):
        """
        Initializes the class to extract geometric components.
        :param ObjectName: String containing the internal name of the object.
        :param Is3D: Boolean. True for 3D solids, False for 2D geometries.
        """
        self.ObjectName = ObjectName
        self.Is3D = Is3D
        self.ActiveDoc = App.ActiveDocument
        self.TargetObj = self.GetObjectByName()

    def GetObjectByName(self):
        """Finds and validates the object within the active document."""
        if not self.ActiveDoc:
            print("Error: No active document found in FreeCAD.")
            return None
        
        FoundObject = self.ActiveDoc.getObject(self.ObjectName)
        if not FoundObject:
            print(f"Error: Object '{self.ObjectName}' not found in the document.")
            return None
            
        if not hasattr(FoundObject, "Shape"):
            print(f"Error: Object '{self.ObjectName}' lacks a valid geometric Shape.")
            return None
            
        return FoundObject

    def Execute(self):
        """Triggers the extraction logic based on the dimensionality flag."""
        if not self.TargetObj:
            return

        TargetShape = self.TargetObj.Shape

        if self.Is3D:
            self.Process3D(TargetShape)
        else:
            self.Process2D(TargetShape)
            
        self.ActiveDoc.recompute()

    def Process3D(self, TargetShape):
        """Extracts faces and edges from 3D solid objects."""
        print(f"Processing '{self.ObjectName}' as a 3D solid...")
        
        # 1. Extract and create all Surfaces / Faces
        for Index, Face in enumerate(TargetShape.Faces):
            FaceName = f"{self.TargetObj.Name}_Surface_{Index+1}"
            NewFace = self.ActiveDoc.addObject("Part::Feature", FaceName)
            NewFace.Shape = Face
            
        # 2. Extract and create all Edges
        for Index, Edge in enumerate(TargetShape.Edges):
            EdgeName = f"{self.TargetObj.Name}_Edge_{Index+1}"
            NewEdge = self.ActiveDoc.addObject("Part::Feature", EdgeName)
            NewEdge.Shape = Edge
            
        print(f"Success: {len(TargetShape.Faces)} surfaces and {len(TargetShape.Edges)} edges created.")

    def Process2D(self, TargetShape):
        """Extracts wireframe edges and unique control vertices from 2D objects."""
        print(f"Processing '{self.ObjectName}' as a 2D geometry...")
        
        # 1. Extract and create all Edges (Lines/Arcs/Splines)
        for Index, Edge in enumerate(TargetShape.Edges):
            LineName = f"{self.TargetObj.Name}_Line_{Index+1}"
            NewLine = self.ActiveDoc.addObject("Part::Feature", LineName)
            NewLine.Shape = Edge
            
        # 2. Extract and create unique Vertices
        UniqueVertices = {}
        for Vertex in TargetShape.Vertices:
            # Rounding to 4 decimal places filters out duplicate overlapping vertex structures
            PositionKey = (round(Vertex.X, 4), round(Vertex.Y, 4), round(Vertex.Z, 4))
            if PositionKey not in UniqueVertices:
                UniqueVertices[PositionKey] = Vertex
                
                VertexName = f"{self.TargetObj.Name}_Point_{len(UniqueVertices)}"
                NewVertex = self.ActiveDoc.addObject("Part::Vertex", VertexName)
                NewVertex.X = Vertex.X
                NewVertex.Y = Vertex.Y
                NewVertex.Z = Vertex.Z
                
        print(f"Success: {len(TargetShape.Edges)} lines and {len(UniqueVertices)} unique points created.")

## example for Batch Implementation
#TargetsToProcess = [
#    {"Name": "Pad", "Is3D": True},
#    {"Name": "ProfileSketch", "Is3D": False}
#]
#
#for Target in TargetsToProcess:
#    Worker = CreateObjects(ObjectName=Target["Name"], Is3D=Target["Is3D"])
#    Worker.Execute()
# Copyright (C) 2026 El Equipo del Proyecto DAV
# Copyright (C) 2026 The DAV Project Team
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

try:
    from .tagger import Tagger
except ImportError:
    try:
        from tagger import Tagger
    except ImportError:
        try:
            from selection.tagger import Tagger
        except ImportError:
            from Dav.scr.selection.tagger import Tagger


class CreateObjects:
    """Extract tacit Part objects from an existing shape using Tagger names.

    When ``AskName`` is true (the default) the user is prompted by voice for a
    name for the source object before it is decomposed, so it can later be
    picked from the tree with ObjectSelection.SelectByLabel.
    """

    def __init__(
        self,
        ObjectName: str,
        Is3D: bool = False,
        *,
        TaggerInstance: Tagger | None = None,
        Language=None,
        AskName: bool = True,
    ) -> None:
        self.ObjectName = ObjectName
        self.Is3D = Is3D
        self.AskName = AskName
        self.ActiveDoc = App.ActiveDocument
        self.Tagger = TaggerInstance or Tagger(Language, self.ActiveDoc)
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

    def Execute(self) -> None:
        """Triggers the extraction logic based on the dimensionality flag."""
        if not self.TargetObj:
            return

        if self.AskName:
            self.RequestName()

        TargetShape = self.TargetObj.Shape

        if self.Is3D:
            self.Process3D(TargetShape)
        else:
            self.Process2D(TargetShape)

        self.ActiveDoc.recompute()

    def RequestName(self) -> str:
        """Ask the user to name the target object before decomposing it.

        Failure to prompt is not fatal: the Tagger's automatic name is used,
        so object creation never gets blocked by the voice layer.
        """
        try:
            try:
                from .nameprompt import AskObjectName
            except ImportError:
                from nameprompt import AskObjectName
            return AskObjectName(self.TargetObj, self.Tagger)
        except Exception as Error:
            print(f"Warning: could not ask for a name ({Error}). Keeping default.")
            return ""

    def Process3D(self, TargetShape) -> None:
        """Extracts faces and edges from 3D solid objects."""
        print(f"Processing '{self.ObjectName}' as a 3D solid...")

        for Face in TargetShape.Faces:
            FaceName = self.Tagger.NextName("surface")
            NewFace = self.ActiveDoc.addObject("Part::Feature", FaceName)
            NewFace.Shape = Face
            self.Tagger.ApplyLabel(NewFace, "surface")

        for Edge in TargetShape.Edges:
            EdgeName = self.Tagger.NextName("edge")
            NewEdge = self.ActiveDoc.addObject("Part::Feature", EdgeName)
            NewEdge.Shape = Edge
            self.Tagger.ApplyLabel(NewEdge, "edge")

        print(
            f"Success: {len(TargetShape.Faces)} surfaces and "
            f"{len(TargetShape.Edges)} edges created."
        )

    def Process2D(self, TargetShape) -> None:
        """Extracts wireframe edges and unique control vertices from 2D objects."""
        print(f"Processing '{self.ObjectName}' as a 2D geometry...")

        for Edge in TargetShape.Edges:
            LineName = self.Tagger.NextName("line")
            NewLine = self.ActiveDoc.addObject("Part::Feature", LineName)
            NewLine.Shape = Edge
            self.Tagger.ApplyLabel(NewLine, "line")

        UniqueVertices = {}
        for Vertex in TargetShape.Vertexes:
            PositionKey = (round(Vertex.X, 4), round(Vertex.Y, 4), round(Vertex.Z, 4))
            if PositionKey not in UniqueVertices:
                UniqueVertices[PositionKey] = Vertex

                VertexName = self.Tagger.NextName("point")
                NewVertex = self.ActiveDoc.addObject("Part::Vertex", VertexName)
                NewVertex.X = Vertex.X
                NewVertex.Y = Vertex.Y
                NewVertex.Z = Vertex.Z
                self.Tagger.ApplyLabel(NewVertex, "point")

        print(
            f"Success: {len(TargetShape.Edges)} lines and "
            f"{len(UniqueVertices)} unique points created."
        )

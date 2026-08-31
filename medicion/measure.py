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
import FreeCADGui as Gui
import Draft
from PySide import QtGui

def CreateDimension():
    # 1. Detect if the active view is 2D or 3D
    ActiveView = Gui.ActiveDocument.ActiveView
    Is2D = False

    if ActiveView is not None:
        IsOrthographic = hasattr(ActiveView, "getCameraType") and (ActiveView.getCameraType() == "Orthographic")
        
        # Check view direction vector (Top/Bottom 2D planar view check)
        if hasattr(ActiveView, "getViewDirection"):
            ViewDir = ActiveView.getViewDirection()
            # If looking straight down/up along the Z-axis: (0, 0, -1) or (0, 0, 1)
            Is2D = IsOrthographic and (abs(round(ViewDir.z, 2)) == 1.0)
        elif hasattr(ActiveView, "getCameraOrientation"):
            Orientation = ActiveView.getCameraOrientation()
            # Base.Rotation.Q returns tuple (x, y, z, w)
            if hasattr(Orientation, "Q"):
                Is2D = IsOrthographic and (abs(round(Orientation.Q[2], 2)) == 1.0)

    DimensionText = "2D" if Is2D else "3D"
    
    # Helper function to request point coordinates from the user
    def RequestPoint(PointName):
        InputLabel = f"Enter coordinates for Point {PointName} ({DimensionText}):"
        DefaultValue = "0, 0" if Is2D else "0, 0, 0"
        InputText, IsOk = QtGui.QInputDialog.getText(None, f"Point {PointName}", InputLabel, text=DefaultValue)
        
        if not IsOk or not InputText:
            return None
        
        try:
            Coordinates = [float(Coord.strip()) for Coord in InputText.split(",")]
            if Is2D and len(Coordinates) == 2:
                return App.Vector(Coordinates[0], Coordinates[1], 0.0)
            elif not Is2D and len(Coordinates) == 3:
                return App.Vector(Coordinates[0], Coordinates[1], Coordinates[2])
            else:
                App.Console.PrintError(f"Error: You must enter {'2' if Is2D else '3'} comma-separated values.\n")
                return None
        except ValueError:
            App.Console.PrintError("Error: Invalid coordinate format.\n")
            return None

    # 2. Request Point 1 and Point 2
    Point1 = RequestPoint("1")
    if Point1 is None: 
        return
    
    Point2 = RequestPoint("2")
    if Point2 is None: 
        return

    # 3. Request dimension offset distance
    OffsetDistance, IsOk = QtGui.QInputDialog.getDouble(
        None, 
        "Dimension Offset", 
        "Enter dimension line extension/offset distance:", 
        value=10.0, 
        decimals=2
    )
    if not IsOk: 
        return

    # 4. Calculate dimension line pass-through point based on offset
    LineVector = Point2.sub(Point1)
    if LineVector.Length == 0:
        App.Console.PrintError("Error: Point 1 and Point 2 coincide.\n")
        return
        
    NormalVector = App.Vector(-LineVector.y, LineVector.x, 0.0)
    if NormalVector.Length == 0:
        NormalVector = App.Vector(0, 0, 1)
    NormalVector.normalize()
    
    DimensionPoint = Point1.add(NormalVector.multiply(OffsetDistance))

    # 5. Create Dimension object
    ActiveDocument = App.ActiveDocument
    ActiveDocument.openTransaction("Create Dimension")
    
    DimensionObject = Draft.make_dimension(Point1, Point2, DimensionPoint)
    
    ActiveDocument.commitTransaction()
    ActiveDocument.recompute()
    App.Console.PrintMessage(f"Dimension successfully created between {Point1} and {Point2}.\n")

# Run in FreeCAD Python console
#CreateDimension()
# ADD INTO A DICTIONARY:
#circle = {
 #   'create': lambda: _execute_with_objects('Sketcher_CreateCircle'),
  #  '3point': lambda: _execute_with_objects('Sketcher_Create3PointCircle'),
   # 'help':   ayuda
   # 'Dimension': lambda: CreateDimension()
#}
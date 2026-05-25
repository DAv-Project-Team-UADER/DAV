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

import FreeCADGui as Gui
import FreeCAD as App
from .ayuda import ayuda

def _create_plane():
    doc = App.activeDocument() or App.newDocument()
    plane = doc.addObject("Part::Plane", "Plane")
    plane.Length = 10
    plane.Width = 10
    doc.recompute()

def _create_point():
    doc = App.activeDocument() or App.newDocument()
    point = doc.addObject("Part::Vertex", "Point")
    doc.recompute()

def _create_tube():
    try:
        from BasicShapes import Shapes
    except ImportError:
        print("Error: Se requiere FreeCAD v0.20+ para usar BasicShapes y crear el Tubo")
        return
    doc = App.activeDocument() or App.newDocument()
    tube = Shapes.addTube(doc, "Tube")
    tube.Height = 10
    tube.InnerRadius = 2
    tube.OuterRadius = 5
    doc.recompute()

primitives = {
    'help': ayuda,
    'plane': _create_plane,
    'point': _create_point,
    'sphere': lambda: Gui.runCommand('Part_Sphere', 0),
    'torus': lambda: Gui.runCommand('Part_Torus', 0),
    'tube': _create_tube
}

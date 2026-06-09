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
from .constraints.constraints import constraints
from .Geometry.line.line import line
from .point.point import point
from .Geometry.polyline.polyline import polyline
from .Geometry.rectangle.rectangle import rectangle
from .square.square import square
from .triangle.triangle import triangle
from .Geometry.circle.circle import circle
from .Geometry.arc.arc import arc
from .Geometry.arc_slot.arc_slot import arc_slot
from .oblong.oblong import oblong
from .text.text import text
from .Geometry.hexagon.hexagon import hexagon
from .Geometry.heptagon.heptagon import heptagon
from .slot.slot import slot
from .Geometry.Ellipse._ellipse import ellipse
from .Geometry.Polygon._polygon import polygon
from .Geometry.BSpline._bspline import bspline
from .Geometry.BSpline_Tools._tools import tools
from .ayuda import ayuda
from .validate.validate import validate
from .tools.tools import tools
from .select.select import select
from .external.external import external
from .view.view import view


sketcher = {
    'line':      line,
    'point':     point,
    'polyline':  polyline,
    'rectangle': rectangle,
    'square':    square,
    'triangle':  triangle,
    'circle':    circle,
    'arc':       arc,
    'slot':      slot,
    'arc_slot':  arc_slot,
    'oblong': oblong,
    'text': text,
    'hexagon': hexagon,
    'heptagon': heptagon,
    'constraints': constraints,
    'ellipse': ellipse,
    'polygon': polygon,
    'bspline': bspline,
    'tools': tools,

    'new': lambda: Gui.runCommand('Sketcher_NewSketch', 0),
    'edit': lambda: Gui.runCommand('Sketcher_EditSketch', 0),
    'attach': lambda: Gui.runCommand('Sketcher_MapSketch', 0),
    'grid': lambda: Gui.runCommand('Sketcher_Grid', 0),
    'stop': lambda: Gui.runCommand('Sketcher_StopOperation', 0),
    'leave': lambda: Gui.runCommand('Sketcher_LeaveSketch', 0),
    'help':      ayuda
}

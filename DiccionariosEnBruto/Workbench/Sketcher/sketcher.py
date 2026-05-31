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

<<<<<<< Updated upstream
=======

import FreeCADGui as Gui
from .constraints.constraints import constraints
from .line.line import line
from .point.point import point
from .polyline.polyline import polyline
from .rectangle.rectangle import rectangle
from .square.square import square
from .triangle.triangle import triangle
from .circle.circle import circle
from .arc.arc import arc
from .arc_slot.arc_slot import arc_slot
from .oblong.oblong import oblong
from .text.text import text
from .hexagon.hexagon import hexagon
from .heptagon.heptagon import heptagon
from .slot.slot import slot
from .Ellipse._ellipse import ellipse
from .Polygon._polygon import polygon
from .BSpline._bspline import bspline
from .BSpline_Tools._tools import tools
>>>>>>> Stashed changes
from .ayuda import ayuda
from .validate.validate import validate
from .tools.tools import tools
from .select.select import select
from .external.external import external
from .view.view import view

<<<<<<< Updated upstream
Sketcher = {
    'help': ayuda,
    'validate': validate,
    'tools': tools,
    'select': select,
    'external': external,
    'view': view
=======

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
    'help':      ayuda,
>>>>>>> Stashed changes
}

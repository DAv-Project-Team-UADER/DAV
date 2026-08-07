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
from .arc.arc import arc
from .arc_slot.arc_slot import arc_slot
from .BSpline.bspline import bspline
from .BSpline_Tools._tools import bspline_tools
from .circle.circle import circle
from .Ellipse._ellipse import ellipse
from .heptagon.heptagon import heptagon
from .hexagon.hexagon import hexagon
from .line.line import line
from .Polygon._polygon import polygon
from .polyline.polyline import polyline
from .rectangle.rectangle import rectangle
from .ayuda import ayuda

geometry = {
    'arc': arc,
    'arc_slot': arc_slot,
    'bspline': bspline,
    'tools': bspline_tools,
    'circle': circle,
    'ellipse': ellipse,
    'heptagon': heptagon,
    'hexagon': hexagon,
    'line': line,
    'polygon': polygon,
    'polyline': polyline,
    'rectangle': rectangle,

    'new': lambda: Gui.runCommand('Sketcher_NewSketch', 0),
    'edit': lambda: Gui.runCommand('Sketcher_EditSketch', 0),
    'attach': lambda: Gui.runCommand('Sketcher_MapSketch', 0),
    'grid': lambda: Gui.runCommand('Sketcher_Grid', 0),
    'stop': lambda: Gui.runCommand('Sketcher_StopOperation', 0),
    'leave': lambda: Gui.runCommand('Sketcher_LeaveSketch', 0),
    'help': ayuda
    }
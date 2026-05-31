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

from .ayuda import ayuda

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
    'new': lambda: Gui.runCommand('Sketcher_NewSketch', 0),
    'edit': lambda: Gui.runCommand('Sketcher_EditSketch', 0),
    'attach': lambda: Gui.runCommand('Sketcher_MapSketch', 0),
    'grid': lambda: Gui.runCommand('Sketcher_Grid', 0),
    'stop': lambda: Gui.runCommand('Sketcher_StopOperation', 0),
    'leave': lambda: Gui.runCommand('Sketcher_LeaveSketch', 0),
    'help':      ayuda,
}

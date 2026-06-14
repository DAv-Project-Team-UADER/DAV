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
from .ayuda import ayuda
from typing import Any
from .validate.validate import validate
from .tools.tools import tools as sketcher_tools
from .select.select import select
from .external.external import external
from .view.view import view
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
from .Geometry.BSpline.bspline import bspline
from .Geometry.BSpline_Tools._tools import bspline_tools


def _toggle_construction(sketch: Any, geo_indices:list[int]):
    """Sketcher_ToggleConstruction — Alterna geometría de construcción.
    sketch: objeto Sketch
    geo_indices: lista de enteros con los índices de geometría
    """
    for idx in geo_indices:
        sketch.toggleConstruction(int(idx))


sketcher = {}
sketcher.update(validate)
sketcher.update(sketcher_tools)
sketcher.update(select)
sketcher.update(external)
sketcher.update(view)
sketcher.update(line)
sketcher.update(point)
sketcher.update(polyline)
sketcher.update(rectangle)
sketcher.update(square)
sketcher.update(triangle)
sketcher.update(circle)
sketcher.update(arc)
sketcher.update(slot)
sketcher.update(arc_slot)
sketcher.update(oblong)
sketcher.update(text)
sketcher.update(hexagon)
sketcher.update(heptagon)
sketcher.update(constraints)
sketcher.update(ellipse)
sketcher.update(polygon)
sketcher.update(bspline)
sketcher.update(bspline_tools)
sketcher.update({
    'new':                lambda: Gui.runCommand('Sketcher_NewSketch', 0),
    'edit':               lambda: Gui.runCommand('Sketcher_EditSketch', 0),
    'attach':             lambda: Gui.runCommand('Sketcher_MapSketch', 0),
    'grid':               lambda: Gui.runCommand('Sketcher_Grid', 0),
    'stop':               lambda: Gui.runCommand('Sketcher_StopOperation', 0),
    'leave':              lambda: Gui.runCommand('Sketcher_LeaveSketch', 0),
    'toggleconstruction': _toggle_construction,
    'cancelediting':      lambda: Gui.runCommand('Sketcher_StopEditing', 0),
    'carboncopy':         lambda: Gui.runCommand('Sketcher_CarbonCopy', 0),
    'copyelements':       lambda: Gui.runCommand('Sketcher_CopyClipboard', 0),
    'cutelements':        lambda: Gui.runCommand('Sketcher_Cut', 0),
    'pasteelements':      lambda: Gui.runCommand('Sketcher_Paste', 0),
    'mirror':             lambda: Gui.runCommand('Sketcher_Symmetry', 0),
    'mirrorsketch':       lambda: Gui.runCommand('Sketcher_MirrorSketch', 0),
    'offset':             lambda: Gui.runCommand('Sketcher_Offset', 0),
    'movearray':          lambda: Gui.runCommand('Sketcher_Translate', 0),
    'rotatepolar':        lambda: Gui.runCommand('Sketcher_Rotate', 0),
    'scale':              lambda: Gui.runCommand('Sketcher_Scale', 0),
    'trimedge':           lambda: Gui.runCommand('Sketcher_Trimming', 0),
    'splitedge':          lambda: Gui.runCommand('Sketcher_Split', 0),
    'extendedge':         lambda: Gui.runCommand('Sketcher_Extend', 0),
    'fillet':             lambda: Gui.runCommand('Sketcher_CreateFillet', 0),
    'chamfer':            lambda: Gui.runCommand('Sketcher_CreateChamfer', 0),
    'help':               ayuda,
})
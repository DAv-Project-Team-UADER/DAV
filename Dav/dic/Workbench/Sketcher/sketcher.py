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
from .Geometry.geometry import geometry
from .arcslot.arcslot import arc_slot as arcslot
from .point.point import point
from .square.square import square
from .triangle.triangle import triangle
from .oblong.oblong import oblong
from .Root.root import root
from .text.text import text
from .slot.slot import slot
from .new_sketch.new_sketch import _new_sketch
from _lenient import LenientDict


def _toggle_construction(sketch: Any, geo_indices:list[int]):
    """Sketcher_ToggleConstruction — Alterna geometría de construcción.
    sketch: objeto Sketch
    geo_indices: lista de enteros con los índices de geometría
    """
    for idx in geo_indices:
        sketch.toggleConstruction(int(idx))


# Subcontextos anidados: el Browser navega por niveles y Sketcher/TraduceTo*.py
# espera sketcher['geometry'], sketcher['point'], ... como submenús (no
# aplanados), igual que Explorer/Explorer.py. Aplanarlos hacía que la clave
# 'create' de line/point/rectangle/circle/... se pisaran entre sí (sobrevivía
# solo la última) y que 'horizontal'/'vertical' de select fueran pisadas por
# las de constraints.
# Las figuras (línea, círculo, rectángulo, polígono...) viven agrupadas en
# Geometry/geometry.py, que ya está anidado correctamente.
sketcher = {}
sketcher.update({'geometry':    geometry})
sketcher.update({'arcslot':     arcslot})
sketcher.update({'constraints': constraints})
sketcher.update({'external':    external})
sketcher.update({'oblong':      oblong})
sketcher.update({'point':       point})
sketcher.update({'root':        root})
sketcher.update({'select':      select})
sketcher.update({'slot':        slot})
sketcher.update({'square':      square})
sketcher.update({'text':        text})
sketcher.update({'tools':       sketcher_tools})
sketcher.update({'triangle':    triangle})
sketcher.update({'validate':    validate})
sketcher.update({'view':        view})
sketcher.update({
    'new':                _new_sketch,
    'edit':               lambda: Gui.runCommand('Sketcher_EditSketch', 0),
    'attach':             lambda: Gui.runCommand('Sketcher_MapSketch', 0),
    'grid':               lambda: Gui.runCommand('Sketcher_Grid', 0),
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

# Tolerante a claves aún no implementadas (no rompe el contexto entero).
sketcher = LenientDict(sketcher)
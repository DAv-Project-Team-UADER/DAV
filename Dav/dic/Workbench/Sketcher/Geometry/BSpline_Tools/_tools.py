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
# SPDX-License-Identifier: GPL-3.0-or-later

import FreeCADGui as Gui
from .ayuda import ayuda


def _select_only(obj):
    """Select a single document object after clearing the selection."""
    Gui.Selection.clearSelection()
    Gui.Selection.addSelection(obj)


def _run_on_selection(obj, command):
    """Select the object dictated by voice and run a Sketcher command on it."""
    _select_only(obj)
    Gui.runCommand(command, 0)


def tonurbs_by_voice(obj: object):
    """Convert a dictated B-Spline geometry into an editable NURBS curve."""
    _run_on_selection(obj, 'Sketcher_BSplineConvertToNURBS')


def decrease_degree_by_voice(obj: object):
    """Decrease the mathematical degree of a dictated B-Spline."""
    _run_on_selection(obj, 'Sketcher_BSplineDecreaseDegree')


def increase_degree_by_voice(obj: object):
    """Increase the mathematical degree of a dictated B-Spline."""
    _run_on_selection(obj, 'Sketcher_BSplineIncreaseDegree')


def insert_knot_by_voice(obj: object, value: float):
    """Insert a knot at a dictated parametric position of a B-Spline.

    Args:
        obj: The B-Spline geometry to modify, selected by voice.
        value: Parametric position (0..1) of the new knot.
    """
    _run_on_selection(obj, 'Sketcher_BSplineInsertKnot')
    print(f"[geometry.bspline_tools] knot position dictated: {value}")


def join_curves_by_voice(obj1: object, obj2: object):
    """Join two dictated B-Spline curves into one continuous curve."""
    Gui.Selection.clearSelection()
    Gui.Selection.addSelection(obj1)
    Gui.Selection.addSelection(obj2)
    Gui.runCommand('Sketcher_BSplineJoinCurve', 0)


bspline_tools = {
    'tonurbs':    tonurbs_by_voice,
    'decrease':   decrease_degree_by_voice,
    'increase':   increase_degree_by_voice,
    'knot':       insert_knot_by_voice,
    'join':       join_curves_by_voice,
    'help':       ayuda,
}
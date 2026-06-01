# Copyright (C) 2026 El Equipo del Proyecto DAV
# Universidad Autónoma de Entre Ríos (UADER)
# Licencia GPL v3

import FreeCADGui as Gui

constraints = {
    'coincident': lambda: Gui.runCommand('Sketcher_ConstrainCoincident', 0),
    'coincident unified': lambda: Gui.runCommand('Sketcher_ConstrainCoincidentUnified', 0),
    'horizontal': lambda: Gui.runCommand('Sketcher_ConstrainHorizontal', 0),
    'vertical': lambda: Gui.runCommand('Sketcher_ConstrainVertical', 0),
    'horizontal vertical': lambda: Gui.runCommand('Sketcher_ConstrainHorVer', 0),
    'parallel': lambda: Gui.runCommand('Sketcher_ConstrainParallel', 0),
    'perpendicular': lambda: Gui.runCommand('Sketcher_ConstrainPerpendicular', 0),
    'tangent collinear': lambda: Gui.runCommand('Sketcher_ConstrainTangent', 0),
    'equal': lambda: Gui.runCommand('Sketcher_ConstrainEqual', 0),
    'symmetric': lambda: Gui.runCommand('Sketcher_ConstrainSymmetric', 0),
    'block': lambda: Gui.runCommand('Sketcher_ConstrainBlock', 0),
    'lock position': lambda: Gui.runCommand('Sketcher_ConstrainLock', 0),
    'point on object': lambda: Gui.runCommand('Sketcher_ConstrainPointOnObject', 0),
    'group': lambda: Gui.runCommand('Sketcher_ConstrainGroup', 0),
    'refraction': lambda: Gui.runCommand('Sketcher_ConstrainRefraction', 0),
    'toggle driving reference': lambda: Gui.runCommand('Sketcher_ToggleDrivingReference', 0),
    'toggle constraints': lambda: Gui.runCommand('Sketcher_ToggleConstraints', 0),
}

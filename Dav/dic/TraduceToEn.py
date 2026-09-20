# Copyright (C) 2026 El Equipo del Proyecto DAV
# Copyright (C) 2026 The DAV Project Team
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

"""English spoken-word mapping for the DAV base dictionary."""

from Workbench.workbench import workbench as Workbench
from StdView.StdView import StdView
from Explorer.Explorer import explorer
from LineAttributes.LineAttributes import LineAttributes
from Selection.selection import selection
from Correction.Correction import correction
from measure import CreateDimension
from integration.dav_dock_panel import hide_dav_panel, show_dav_panel
from integration.launch_preferences import open_preferences

TraduceToEn = {
    "explorer":    explorer,
    "file":        explorer,
    "files":       explorer,
    "folder":      explorer,
    "folders":     explorer,
    "directory":   explorer,
    "directories": explorer,
    "workbench":   Workbench,

    "line attributes": LineAttributes,
    "line attributes dialog": LineAttributes,
    "line attributes window": LineAttributes,
    "line attributes panel": LineAttributes,

    "Std View": StdView,
    "standard view": StdView,
    "standard views": StdView,
    "standard view dialog": StdView,
    "standard view window": StdView,

    "workbench":   Workbench,
    "work":   Workbench,
    "workbenches": Workbench,
    "workbench dialog": Workbench,
    "workbench window": Workbench,

    "selection":         selection,
    "select":            selection,
    "object selection":  selection,
    "selected objects":  selection,
    "objects":           selection,
    "preferences": open_preferences,
    "settings":    open_preferences,

    # DAV panel
    "minimize":   hide_dav_panel,
    "hide panel": hide_dav_panel,
    "maximize":   show_dav_panel,
    "show panel": show_dav_panel,

    # Corrections (global: can be said from any context)
    "undo":              correction["undo"],
    "undo change":       correction["undo"],
    "redo":              correction["redo"],
    "redo change":       correction["redo"],
    "delete last":       correction["deletelast"],
    "remove last":       correction["deletelast"],
    "delete last object": correction["deletelast"],
    "delete object":     correction["deleteobject"],
    "remove object":     correction["deleteobject"],
    "delete broken":     correction["deletebroken"],
    "remove broken":     correction["deletebroken"],
    "clean broken":      correction["deletebroken"],
    "clean errors":      correction["deletebroken"],

    # Dimension / measure (global: Vosk only hears the root and the current context)
    "measure":          CreateDimension,
    "measure distance": CreateDimension,
    "dimensioning":     CreateDimension,
    "tape measure":     CreateDimension,
}

# Vistas estándar (frontal, arriba, zoom...): en todos los contextos, raíz incluida
from dic.StdView.StandardViews.TraduceToEn import TraduceToEn as _StandardViewsPhrases
for _phrase, _target in _StandardViewsPhrases.items():
    TraduceToEn.setdefault(_phrase, _target)

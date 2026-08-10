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
    "workbenches": Workbench,
    "workbench dialog": Workbench,
    "workbench window": Workbench,

    "preferences": open_preferences,
    "settings":    open_preferences,
}

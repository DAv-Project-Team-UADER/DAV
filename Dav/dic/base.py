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

"""
Base dictionary — top-level commands available at all times.

  'explorer'        → archivo, edición, ventanas (submenu)
  'stdview'         → vistas estándar, cámara, apariencia (submenu)
  'workbench'       → PartDesign, Draft, Sketcher, Part, Assembly, TechDraw (submenu)
  'lineattributes'  → atributos de línea (submenu)
  'selection'       → navegación de objetos por voz (submenu)
  'preferences'     → abre el diálogo de preferencias DAV
"""

from Explorer.Explorer import explorer
from StdView.StdView import StdView
from Workbench.workbench import workbench
from LineAttributes.LineAttributes import LineAttributes
from Selection.selection import selection
from integration.launch_preferences import open_preferences

Base = {
    "explorer":       explorer,
    "stdview":        StdView,
    "workbench":      workbench,
    "lineattributes": LineAttributes,
    "selection":      selection,
    "preferences":    open_preferences,
}

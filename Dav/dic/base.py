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

  'explorer'    → archivo, edición, ventanas (submenu)
  'preferences' → abre el diálogo de preferencias DAV

TODO equipo: agregar los workbenches (PartDesign, Draft, TechDraw, etc.)
cuando los TraduceTo*.py de cada carpeta estén completos.
"""

from Explorer.Explorer import explorer
from Workbench.workbench import workbench as Workbench
from Workbench.Part.Part import part
from Workbench.Part.circle.circle import circle
from integration.launch_preferences import open_preferences

Base = {
    "explorer":    explorer,
    "mesa de trabajo": Workbench,
    "banco de trabajo": Workbench,
    "workbench":   Workbench,
    "pieza":       part,
    "part":        part,
    "circulo":     circle["circle"],
    "círculo":     circle["circle"],
    "preferences": open_preferences,
}

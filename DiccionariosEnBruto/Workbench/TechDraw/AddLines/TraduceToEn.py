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

import FreeCADGui as Gui
from .ayuda import ayuda

TraduceToEn = {
    'two lines':         lambda: Gui.runCommand('TechDraw_2LineCenterLine', 0),
    'two line center':   lambda: Gui.runCommand('TechDraw_2LineCenterLine', 0),  # synonym
    'center line':       lambda: Gui.runCommand('TechDraw_2LineCenterLine', 0),  # synonym
    'two points':        lambda: Gui.runCommand('TechDraw_2PointCenterLine', 0),
    'two point center':  lambda: Gui.runCommand('TechDraw_2PointCenterLine', 0),  # synonym
    'point center line': lambda: Gui.runCommand('TechDraw_2PointCenterLine', 0),  # synonym
    'cosmetic':          lambda: Gui.runCommand('TechDraw_2PointCosmeticLine', 0),
    'cosmetic line':     lambda: Gui.runCommand('TechDraw_2PointCosmeticLine', 0),  # synonym
    'construction line': lambda: Gui.runCommand('TechDraw_2PointCosmeticLine', 0),  # synonym
    'decorate':          lambda: Gui.runCommand('TechDraw_DecorateLine', 0),
    'line style':        lambda: Gui.runCommand('TechDraw_DecorateLine', 0),  # synonym
    'change line':       lambda: Gui.runCommand('TechDraw_DecorateLine', 0),  # synonym
    'center':            lambda: Gui.runCommand('TechDraw_FaceCenterLine', 0),
    'face center':       lambda: Gui.runCommand('TechDraw_FaceCenterLine', 0),  # synonym
    'face center line':  lambda: Gui.runCommand('TechDraw_FaceCenterLine', 0),  # synonym
    'help':              ayuda,
    'assistance':        ayuda,  # synonym
}

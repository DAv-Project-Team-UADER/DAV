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

"""
Workbench module that aggregates all FreeCAD workbenches.
Combines Assembly, DraftWork, Part, PartDesign, Sketcher, and TechDraw workbenches.
"""

import FreeCADGui as Gui
from .Assembly.Assembly import assembly
from .DraftWork.DraftWork import draft
from .Part.Part import part
from .PartDesign.partdesign import partdesign
from .Sketcher.sketcher import sketcher
from .TechDraw.TechDraw import techdraw
from .ayuda import ayuda

workbench = {}
workbench.update(assembly)
workbench.update(draft)
workbench.update(part)
workbench.update(partdesign)
workbench.update(sketcher)
workbench.update(techdraw)
workbench.update({'help': ayuda})

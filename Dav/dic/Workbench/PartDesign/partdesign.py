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
from .base.base import base
from .additive.additive import additive
from .subtractive.subtractive import subtractive
from .modify.modify import modify
from .transform.transform import transform
from .manage.manage import manage
from .ayuda import ayuda
from _lenient import LenientDict

# Subcontextos anidados: el Browser navega por niveles y
# PartDesign/TraduceTo*.py espera partdesign['base'], partdesign['additive'],
# ... como submenús (no aplanados), igual que Explorer/Explorer.py.
partdesign = {}
partdesign.update({'base':        base})
partdesign.update({'additive':    additive})
partdesign.update({'subtractive': subtractive})
partdesign.update({'modify':      modify})
partdesign.update({'transform':   transform})
partdesign.update({'manage':      manage})
partdesign.update({'help': ayuda})

# Tolerante a claves aún no implementadas (no rompe el contexto entero).
partdesign = LenientDict(partdesign)

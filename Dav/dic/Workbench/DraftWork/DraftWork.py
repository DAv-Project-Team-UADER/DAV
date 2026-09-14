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
from .annotation_style_editor.annotation_style_editor import annotation
from .arc.arc import arc
from .curve.curve import curve
from .circle.circle import circle
from .circular_array.circular_array import array
from .modify.modify import modify
from .dimension.dimension import dimension
from .ellipse.ellipse import ellipse
from .facebinder.facebinder import facebinder
from .Drafting.drafting import drafting
from .creation.creation import creation
from .modification.modification import modification
from .pointplacement.pointplacement import pointplacement
from .pointconnect.pointconnect import pointconnect
from .ayuda import ayuda
from _lenient import LenientDict

# Subcontextos anidados: el Browser navega por niveles y
# DraftWork/TraduceTo*.py espera draft['annotation'], draft['arc'], ... como
# submenús (no aplanados), igual que Explorer/Explorer.py. Aplanarlos hacía
# que la clave 'center' de arc/circle fuera pisada por la de ellipse.
draft = {}
draft.update({'annotation':     annotation})
draft.update({'arc':            arc})
draft.update({'curve':          curve})
draft.update({'circle':         circle})
draft.update({'array':          array})
draft.update({'modify':         modify})
draft.update({'dimension':      dimension})
draft.update({'ellipse':        ellipse})
draft.update({'facebinder':     facebinder})
draft.update({'drafting':       drafting})
draft.update({'creation':       creation})
draft.update({'modification':   modification})
draft.update({'pointplacement': pointplacement})
draft.update({'pointconnect':   pointconnect})
draft.update({'help': ayuda})

# Tolerante a claves aún no implementadas (no rompe el contexto entero).
draft = LenientDict(draft)
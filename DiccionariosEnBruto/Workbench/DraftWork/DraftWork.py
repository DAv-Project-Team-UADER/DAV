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
from .ayuda import ayuda
from _lenient import LenientDict

draft = {}
draft.update(annotation)
draft.update(arc)
draft.update(curve)
draft.update(circle)
draft.update(array)
draft.update(modify)
draft.update(dimension)
draft.update(ellipse)
draft.update(facebinder)
draft.update(drafting)
draft.update(creation)
draft.update(modification)
draft.update({'help': ayuda})

# Tolerante a claves aún no implementadas (no rompe el contexto entero).
draft = LenientDict(draft)
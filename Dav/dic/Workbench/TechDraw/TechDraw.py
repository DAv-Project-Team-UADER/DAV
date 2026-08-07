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

from .Views.Views               import views
from .Dimensions.dimensions     import dimensions
from .AddLines.addLines         import addLines
from .Symbols.Symbols           import symbols
from .Snaps.Snaps               import snaps
from .Topology.Topology         import topology
from .Page.Page                 import page
from .Annotations.annotations   import annotations
from .Hatching.hatching         import hatching
from .AddVertices.addVertices   import add_vertices
from .OtherViews.otherViews     import other_views
from .Features.Features         import features
from .ayuda import ayuda

# Subcontextos anidados: el Browser navega por niveles y espera
# techdraw['views'], techdraw['dimensions'], ... como submenús (no aplanados),
# igual que Explorer/Explorer.py. Aplanarlos hacía que la clave 'cosmetic' de
# addLines fuera pisada por la de add_vertices.
techdraw = {}
techdraw.update({'views':       views})
techdraw.update({'dimensions':  dimensions})
techdraw.update({'addlines':    addLines})
techdraw.update({'symbols':     symbols})
techdraw.update({'snaps':       snaps})
techdraw.update({'topology':    topology})
techdraw.update({'page':        page})
techdraw.update({'annotations': annotations})
techdraw.update({'hatching':    hatching})
techdraw.update({'addvertices': add_vertices})
techdraw.update({'otherviews':  other_views})
techdraw.update({'features':    features})
techdraw.update({'help': ayuda})
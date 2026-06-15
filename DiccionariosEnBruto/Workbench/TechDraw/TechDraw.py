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
from .Dimensions.Dimensions     import dimensions
from .AddLines.AddLines         import addLines
from .Symbols.Symbols           import symbols
from .Snaps.Snaps               import snaps
from .Topology.Topology         import topology
from .Page.Page                 import page
from .Annotations.Annotations   import annotations
from .Hatching.Hatching         import hatching
from .AddVertices.AddVertices   import add_vertices
from .OtherViews.OtherViews     import other_views
from .Features.Features         import features
from .ayuda import ayuda

techdraw = {}
techdraw.update(views)
techdraw.update(dimensions)
techdraw.update(addLines)
techdraw.update(symbols)
techdraw.update(snaps)
techdraw.update(topology)
techdraw.update(page)
techdraw.update(annotations)
techdraw.update(hatching)
techdraw.update(add_vertices)
techdraw.update(other_views)
techdraw.update(features)
techdraw.update({'ayuda': ayuda})
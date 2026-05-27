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

from .Appearance.Appearance       import appearance
from .Camera.Camera               import camera
from .DrawStyles.DrawStyles       import drawstyles
from .Overlay.Overlay             import overlay
from .Panels.Panels               import panels
from .SavedViews.SavedViews       import savedviews
from .StandardViews.StandardViews import standardviews
from .Stereo.Stereo               import stereo
from .Toolbars.Toolbars           import toolbars
from .Tree.Tree                   import tree
from .Visibility.Visibility       import visibility
from .ayuda                       import ayuda

stdview = {}
stdview.update(appearance)
stdview.update(camera)
stdview.update(drawstyles)
stdview.update(overlay)
stdview.update(panels)
stdview.update(savedviews)
stdview.update(standardviews)
stdview.update(stereo)
stdview.update(toolbars)
stdview.update(tree)
stdview.update(visibility)
stdview.update({'ayuda': ayuda})

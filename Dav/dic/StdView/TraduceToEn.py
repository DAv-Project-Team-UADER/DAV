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

"""English spoken-word mapping for the DAV StdView dictionary folders."""

from .Appearance.Appearance import appearance
from .Camera.Camera import camera
from .Clipping.Clipping import clipping
from .DrawStyles.DrawStyles import drawstyles
from .Material.Material import material
from .Overlay.Overlay import overlay
from .Panels.Panels import Panels
from .SavedViews.SavedViews import savedviews
from .StandardViews.StandardViews import StandardViews
from .Stereo.Stereo import stereo
from .Toolbars.Toolbars import toolbars
from .Tree.Tree import tree
from .Visibility.Visibility import visibility
from .ayuda import ayuda

TraduceToEn = {
    "appearance": appearance,
    "visual appearance": appearance,
    "look": appearance,

    "camera": camera,
    "view camera": camera,

    "clipping": clipping,
    "clip": clipping,
    "clipping plane": clipping,

    "draw styles": drawstyles,
    "drawing styles": drawstyles,
    "display styles": drawstyles,
    "visual styles": drawstyles,

    "material": material,
    "materials": material,

    "overlay": overlay,
    "overlays": overlay,
    "overlay view": overlay,

    "panels": Panels,
    "panel": Panels,
    "view panels": Panels,

    "saved views": savedviews,
    "saved view": savedviews,
    "bookmarked views": savedviews,

    "standard views": StandardViews,
    "standard view": StandardViews,
    "basic views": StandardViews,

    "stereo": stereo,
    "stereoscopic": stereo,
    "stereo view": stereo,

    "toolbars": toolbars,
    "toolbar": toolbars,
    "view toolbars": toolbars,

    "tree": tree,
    "model tree": tree,
    "document tree": tree,

    "visibility": visibility,
    "visible": visibility,
    "show hide": visibility,

    "help": ayuda,
    "manual": ayuda,
    "support": ayuda,
    "documentation": ayuda,
}

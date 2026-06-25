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

from DAV.DiccionariosEnBruto.StdView.StdView import StdView

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
    "appearance": StdView["appearance"],
    "visual appearance": StdView["appearance"],
    "look": StdView["appearance"],

    "camera": StdView["camera"],
    "view camera": StdView["camera"],

    "clipping": StdView["clipping"],
    "clip": StdView["clipping"],
    "clipping plane": StdView["clipping"],

    "draw styles": StdView["drawstyles"],
    "drawing styles": StdView["drawstyles"],
    "display styles": StdView["drawstyles"],
    "visual styles": StdView["drawstyles"],

    "material": StdView["material"],
    "materials": StdView["material"],

    "overlay": StdView["overlay"],
    "overlays": StdView["overlay"],
    "overlay view": StdView["overlay"],

    "panels": StdView["panels"],
    "panel": StdView["panels"],
    "view panels": StdView["panels"],

    "saved views": StdView["savedviews"],
    "saved view": StdView["savedviews"],
    "bookmarked views": StdView["savedviews"],

    "standard views": StdView["standardviews"],
    "standard view": StdView["standardviews"],
    "basic views": StdView["standardviews"],

    "stereo": StdView["stereo"],
    "stereoscopic": StdView["stereo"],
    "stereo view": StdView["stereo"],

    "toolbars": StdView["toolbars"],
    "toolbar": StdView["toolbars"],
    "view toolbars": StdView["toolbars"],

    "tree": StdView["tree"],
    "model tree": StdView["tree"],
    "document tree": StdView["tree"],

    "visibility": StdView["visibility"],
    "visible": StdView["visibility"],
    "show hide": StdView["visibility"],

    "help": StdView["help"],
    "info": StdView["help"],
    "options": StdView["help"],
}

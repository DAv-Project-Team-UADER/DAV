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

# ayuda.py - StdView (Corregido con rutas de importación relativas)

from .Appearance.ayuda import ayuda as ayuda_appearance
from .Camera.ayuda import ayuda as ayuda_camera
from .Clipping.ayuda import ayuda as ayuda_clipping
from .DrawStyles.ayuda import ayuda as ayuda_drawstyles
from .Material.ayuda import ayuda as ayuda_material
from .Overlay.ayuda import ayuda as ayuda_overlay
from .Panels.ayuda import ayuda as ayuda_panels
from .SavedViews.ayuda import ayuda as ayuda_savedviews
from .StandardViews.ayuda import ayuda as ayuda_standardviews
from .Stereo.ayuda import ayuda as ayuda_stereo
from .Toolbars.ayuda import ayuda as ayuda_toolbars
from .Tree.ayuda import ayuda as ayuda_tree
from .Visibility.ayuda import ayuda as ayuda_visibility

def ayuda():
    print("=== StdView - Comandos de Vista ===")
    ayuda_appearance()
    ayuda_camera()
    ayuda_clipping()
    ayuda_drawstyles()
    ayuda_material()
    ayuda_overlay()
    ayuda_panels()
    ayuda_savedviews()
    ayuda_standardviews()
    ayuda_stereo()
    ayuda_toolbars()
    ayuda_tree()
    ayuda_visibility()
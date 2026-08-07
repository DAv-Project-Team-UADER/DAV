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
from .Clipping.Clipping           import clipping
from .DrawStyles.DrawStyles       import drawstyles
from .Material.Material           import material
from .Overlay.Overlay             import overlay
from .Panels.Panels               import Panels
from .SavedViews.SavedViews       import savedviews
from .StandardViews.StandardViews import StandardViews
from .Stereo.Stereo               import stereo
from .Toolbars.Toolbars           import toolbars
from .Tree.Tree                   import tree
from .Visibility.Visibility       import visibility
from .ayuda                       import ayuda

# Diccionario maestro del módulo StdView.
# Subcontextos anidados: el Browser navega por niveles y StdView/TraduceTo*.py
# espera StdView['camera'], StdView['panels'], ... como submenús (no aplanados),
# igual que Explorer/Explorer.py. Aplanarlos hacía que 'bottom'/'left'/'right'
# de Overlay pisaran los de StandardViews y que 'toggle' de Overlay pisara el
# de Visibility.
StdView = {}
StdView.update({'appearance':     appearance})
StdView.update({'camera':         camera})
StdView.update({'clipping':       clipping})
StdView.update({'drawstyles':     drawstyles})
StdView.update({'material':       material})
StdView.update({'overlay':        overlay})
StdView.update({'panels':         Panels})
StdView.update({'savedviews':     savedviews})
StdView.update({'standardviews':  StandardViews})
StdView.update({'stereo':         stereo})
StdView.update({'toolbars':       toolbars})
StdView.update({'tree':           tree})
StdView.update({'visibility':     visibility})
StdView.update({'help': ayuda})
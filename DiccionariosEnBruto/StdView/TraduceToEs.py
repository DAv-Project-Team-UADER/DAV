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

"""Spanish spoken-word mapping for the DAV StdView dictionary folders."""

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

TraduceToEs = {
    "apariencia": appearance,
    "aspecto": appearance,
    "estilo visual": appearance,

    "camara": camera,
    "cámara": camera,
    "vista de camara": camera,
    "vista de cámara": camera,

    "recorte": clipping,
    "clip": clipping,
    "plano de recorte": clipping,

    "estilos de dibujo": drawstyles,
    "estilos de visualizacion": drawstyles,
    "estilos de visualización": drawstyles,
    "modos de dibujo": drawstyles,

    "material": material,
    "materiales": material,

    "superposicion": overlay,
    "superposición": overlay,
    "overlay": overlay,
    "vista superpuesta": overlay,

    "paneles": Panels,
    "panel": Panels,
    "paneles de vista": Panels,

    "vistas guardadas": savedviews,
    "vista guardada": savedviews,
    "vistas favoritas": savedviews,

    "vistas estandar": StandardViews,
    "vistas estándar": StandardViews,
    "vista estandar": StandardViews,
    "vista estándar": StandardViews,
    "vistas basicas": StandardViews,
    "vistas básicas": StandardViews,

    "estereo": stereo,
    "estéreo": stereo,
    "vista estereo": stereo,
    "vista estéreo": stereo,

    "barras de herramientas": toolbars,
    "barra de herramientas": toolbars,
    "toolbars": toolbars,

    "arbol": tree,
    "árbol": tree,
    "arbol del modelo": tree,
    "árbol del modelo": tree,
    "arbol de documento": tree,
    "árbol de documento": tree,

    "visibilidad": visibility,
    "visible": visibility,
    "mostrar ocultar": visibility,

    "ayuda": ayuda,
    "manual": ayuda,
    "soporte": ayuda,
    "documentacion": ayuda,
    "documentación": ayuda,
    "help": ayuda,
}

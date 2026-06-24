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

"""Portuguese spoken-word mapping for the DAV StdView dictionary folders."""

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

TraduceToPt = {
    "aparencia": appearance,
    "aparência": appearance,
    "aspecto": appearance,
    "estilo visual": appearance,

    "camera": camera,
    "câmera": camera,
    "camara": camera,
    "câmara": camera,
    "vista da camera": camera,
    "vista da câmera": camera,

    "recorte": clipping,
    "clip": clipping,
    "plano de recorte": clipping,

    "estilos de desenho": drawstyles,
    "estilos de visualizacao": drawstyles,
    "estilos de visualização": drawstyles,
    "modos de desenho": drawstyles,

    "material": material,
    "materiais": material,

    "sobreposicao": overlay,
    "sobreposição": overlay,
    "overlay": overlay,
    "vista sobreposta": overlay,

    "paineis": Panels,
    "painéis": Panels,
    "painel": Panels,
    "paineis de vista": Panels,
    "painéis de vista": Panels,

    "vistas salvas": savedviews,
    "vista salva": savedviews,
    "vistas guardadas": savedviews,

    "vistas padrao": StandardViews,
    "vistas padrão": StandardViews,
    "vista padrao": StandardViews,
    "vista padrão": StandardViews,
    "vistas basicas": StandardViews,
    "vistas básicas": StandardViews,

    "estereo": stereo,
    "estéreo": stereo,
    "vista estereo": stereo,
    "vista estéreo": stereo,

    "barras de ferramentas": toolbars,
    "barra de ferramentas": toolbars,
    "toolbars": toolbars,

    "arvore": tree,
    "árvore": tree,
    "arvore do modelo": tree,
    "árvore do modelo": tree,
    "arvore do documento": tree,
    "árvore do documento": tree,

    "visibilidade": visibility,
    "visivel": visibility,
    "visível": visibility,
    "mostrar ocultar": visibility,

    "ajuda": ayuda,
    "manual": ayuda,
    "suporte": ayuda,
    "documentacao": ayuda,
    "documentação": ayuda,
    "help": ayuda,
}

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

from .StdView import StdView

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
from measure import CreateDimension

TraduceToPt = {
    "aparencia": StdView["appearance"],
    "aparência": StdView["appearance"],
    "aspecto": StdView["appearance"],
    "estilo visual": StdView["appearance"],

    "camera": StdView["camera"],
    "câmera": StdView["camera"],
    "camara": StdView["camera"],
    "câmara": StdView["camera"],
    "vista da camera": StdView["camera"],
    "vista da câmera": StdView["camera"],

    "recorte": StdView["clipping"],
    "clip": StdView["clipping"],
    "plano de recorte": StdView["clipping"],

    "estilos de desenho": StdView["drawstyles"],
    "estilos de visualizacao": StdView["drawstyles"],
    "estilos de visualização": StdView["drawstyles"],
    "modos de desenho": StdView["drawstyles"],

    "material": StdView["material"],
    "materiais": StdView["material"],

    "sobreposicao": StdView["overlay"],
    "sobreposição": StdView["overlay"],
    "overlay": StdView["overlay"],
    "vista sobreposta": StdView["overlay"],

    "paineis": StdView["panels"],
    "painéis": StdView["panels"],
    "painel": StdView["panels"],
    "paineis de vista": StdView["panels"],
    "painéis de vista": StdView["panels"],

    "vistas salvas": StdView["savedviews"],
    "vista salva": StdView["savedviews"],
    "vistas guardadas": StdView["savedviews"],

    "vistas padrao": StdView["standardviews"],
    "vistas padrão": StdView["standardviews"],
    "vista padrao": StdView["standardviews"],
    "vista padrão": StdView["standardviews"],
    "vistas basicas": StdView["standardviews"],
    "vistas básicas": StdView["standardviews"],

    "estereo": StdView["stereo"],
    "estéreo": StdView["stereo"],
    "vista estereo": StdView["stereo"],
    "vista estéreo": StdView["stereo"],

    "barras de ferramentas": StdView["toolbars"],
    "barra de ferramentas": StdView["toolbars"],
    "toolbars": StdView["toolbars"],

    "arvore": StdView["tree"],
    "árvore": StdView["tree"],
    "arvore do modelo": StdView["tree"],
    "árvore do modelo": StdView["tree"],
    "arvore do documento": StdView["tree"],
    "árvore do documento": StdView["tree"],

    "visibilidade": StdView["visibility"],
    "visivel": StdView["visibility"],
    "visível": StdView["visibility"],
    "mostrar ocultar": StdView["visibility"],

    "ajuda": StdView["help"],
    "informação": StdView["help"],
    "opções": StdView["help"],

    # MEASURE
    "medir": CreateDimension,
    "medida": CreateDimension,
    "medir distancia": CreateDimension,
    "medir distância": CreateDimension,
    "distância": CreateDimension,
    "distancia": CreateDimension,
    "cotar": CreateDimension,
    "dimensionar": CreateDimension,
    "aferir": CreateDimension,
    "mensurar": CreateDimension,
    "calcular distância": CreateDimension,
    "calcular distancia": CreateDimension,
    "comprimento": CreateDimension,
    "separação": CreateDimension,
    "separacao": CreateDimension,
    "afastamento": CreateDimension,
    "extensão": CreateDimension,
    "extensao": CreateDimension,
    "cota": CreateDimension,
    "cotagem": CreateDimension,
    "acotação": CreateDimension,
    "acotacao": CreateDimension,
    "dimensão": CreateDimension,
    "dimensao": CreateDimension,
    "métrica": CreateDimension,
    "metrica": CreateDimension,
    "dimensionamento": CreateDimension,
    "metro": CreateDimension,
    "milímetro": CreateDimension,
    "milimetro": CreateDimension,
    "centímetro": CreateDimension,
    "centimetro": CreateDimension,
    "flexômetro": CreateDimension,
    "flexometro": CreateDimension,
    "metro enrolável": CreateDimension,
    "metro enrolavel": CreateDimension,
    "régua": CreateDimension,
    "regua": CreateDimension,
    "escalímetro": CreateDimension,
    "escalimetro": CreateDimension,
    "calibre": CreateDimension,
    "paquímetro": CreateDimension,
    "paquimetro": CreateDimension,
    "micrômetro": CreateDimension,
    "micrometro": CreateDimension,
    "tolerância": CreateDimension,
    "tolerancia": CreateDimension,
    "desvio": CreateDimension,
    "ajuste": CreateDimension,
    "medição": CreateDimension,
    "medicao": CreateDimension,
    "mensuração": CreateDimension,
    "mensuracao": CreateDimension,
    "aferição": CreateDimension,
    "afericao": CreateDimension,
    "calibração": CreateDimension,
    "calibracao": CreateDimension,
    "verificação": CreateDimension,
    "verificacao": CreateDimension,
    "inspeção": CreateDimension,
    "inspecao": CreateDimension,
    "controle dimensional": CreateDimension,
    "metrologia": CreateDimension,
}
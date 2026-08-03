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
# SPDX-License-Identifier: GPL-3.0-or-later

"""Portuguese spoken-word mapping for the StdViews Panels dictionary."""

from .Panels import Panels
from .ayuda import ayuda

TraduceToPt = {
    
    # Vistas de Painel e Acoplamento
    "painel": Panels['panel'],
    "vista de painel": Panels['panel'],
    "acoplar": Panels['dock'],
    "vista acoplada": Panels['dock'],
    "desacoplar": Panels['undock'],
    "vista desacoplada": Panels['undock'],
    
    # Tela cheia
    "tela cheia": Panels['fullscreen'],
    "ver tela cheia": Panels['fullscreen'],
    
    # Painéis específicos do FreeCAD
    "vista dag": Panels['dagview'],
    "vista combo": Panels['comboview'],
    "painel combo": Panels['comboview'],
    "vista combinada": Panels['comboview'],
    "painel combinado": Panels['comboview'],
    "vista de selecao": Panels['selectionview'],
    "painel de selecao": Panels['selectionview'],
    "vista de tarefas": Panels['tasks'],
    "tarefas": Panels['tasks'],
    "painel de tarefas": Panels['tasks'],
    "vista de propriedades": Panels['properties'],
    "propriedades": Panels['properties'],
    "painel de propriedades": Panels['properties'],
    "vista de arvore": Panels['treeview'],
    "arvore do modelo": Panels['treeview'],
    
    # Consoles e Barras
    "console python": Panels['console'],
    "console": Panels['console'],
    "vista de relatorio": Panels['report'],
    "relatorio": Panels['report'],
    "barra de status": Panels['statusbar'],

    "ajuda": Panels['help'],
    "informação": Panels['help'],
    "opções": Panels['help']
}
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

"""Portuguese spoken-word mapping for the Sketcher tools dictionary."""

from .tools import tools
from .ayuda import ayuda

TraduceToPt = {
    
    # Deletar restrições e sinônimos
    "apagar restricoes": tools['deleteconstraints'],
    "limpar restricoes": tools['deleteconstraints'],
    "remover restricoes": tools['deleteconstraints'],
    
    # Deletar geometria e sinônimos
    "apagar geometria": tools['deletegeometry'],
    "limpar geometria": tools['deletegeometry'],
    "apagar esboco": tools['deletegeometry'],
    
    # Mesclar e sinônimos
    "mesclar": tools['merge'],
    "mesclar esbocos": tools['merge'],
    "combinar esbocos": tools['merge'],
    
    # Reorientar e sinônimos
    "reorientar": tools['reorient'],
    "reorientar esboco": tools['reorient'],
    "alterar plano do esboco": tools['reorient'],
    
    # Remover alinhamento de eixos e sinônimos
    "remover eixos": tools['removeaxes'],
    "limpar alinhamento de eixos": tools['removeaxes'],

    "ajuda": tools['help'],
    "informação": tools['help'],
    "opções": tools['help']
}
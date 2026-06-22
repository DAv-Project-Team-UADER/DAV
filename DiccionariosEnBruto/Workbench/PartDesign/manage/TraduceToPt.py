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

import manage as manage
import ayuda as ayuda

TraduceToPt= {
    #Mover recurso
    'mover recurso':       manage['movefeature'],
    'mover recurso para corpo':       manage['movefeature'],

    #Mover recurso na árvore
    'mover recurso na árvore': manage['movefeatureintree'],
    'mover recurso para corpo na árvore': manage['movefeatureintree'],

    #Mover ponta
    'mover ponta': manage['movetip'],
    'mover ponta para corpo': manage['movetip'],

    #Preferências
    'preferências': manage['preferences'],
    'Opções': manage['preferences'],

    #Assistente de eixo
    'assistente de eixo': manage['wizardshaft'],
    'assistente de eixo para corpo': manage['wizardshaft'],

    "ajuda":             manage["help"],
    "informação":       manage["help"],
    "opções":            manage["help"]

}

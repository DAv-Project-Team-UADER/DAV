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
# SPDX-License-Identifier: GPL-3.0-or-later"""Portuguese spoken-word mapping for the overlay dictionary."""

from .overlay import overlay

TraduceToPt = {
    # Posições e exibição de sobreposição (overlay)
    'abaixo':                   overlay['bottom'],
    'fundo':                    overlay['bottom'],
    'painel inferior':          overlay['bottom'],

    'flutuar':                  overlay['float'],
    'painel flutuante':         overlay['float'],
    'sobreposicao flutuante':   overlay['float'],

    'esquerda':                 overlay['left'],
    'painel esquerdo':          overlay['left'],
    'sobreposicao esquerda':    overlay['left'],

    'direita':                  overlay['right'],
    'painel direito':           overlay['right'],
    'sobreposicao direita':     overlay['right'],

    'eixo':                     overlay['axis'],
    'cruz de eixos':            overlay['axis'],
    'mostrar eixos':            overlay['axis'],

    'navegacao':                overlay['navigation'],
    'alternar navegacao':       overlay['navigation'],
    'painel de navegacao':      overlay['navigation'],

    'alternar':                 overlay['toggle'],
    'alternar sobreposicao':    overlay['toggle'],
    'mostrar painel':           overlay['toggle'],

    # Comandos de ajuda estandarizados
    'ajuda':                    overlay['help'],
    'comandos':                 overlay['help'],
    'opções':                   overlay['help']
}

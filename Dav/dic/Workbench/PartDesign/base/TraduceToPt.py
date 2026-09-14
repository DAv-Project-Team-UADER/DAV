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

from .base import base
from .ayuda import ayuda

TraduceToPt = {
    #Corpo
    'corpo':           base['body'],
    'Corpo Sólido':           base['body'],

    #Esboço
    'esboco':          base['newsketch'],
    'esboço':          base['newsketch'],
    'esboço novo':          base['newsketch'],
    'esboço novo em plano':          base['newsketch'],
    'esboço novo em face':          base['newsketch'],
    'esboço novo em plano de trabalho':          base['newsketch'],

    #Clonar
    'clonar':          base['clone'],
    'clonar recurso':          base['clone'],
    'clonar recurso para corpo':          base['clone'],

    #Ligação de subforma
    'ligação de subforma': base['subshapebinder'],
    'ligação de subforma para corpo': base['subshapebinder'],
    'vinculação de subforma': base['subshapebinder'],
    'vinculação de subforma para corpo': base['subshapebinder'],

    "ajuda":             base["help"],
    "informação":       base["help"],
    "opções":            base["help"]
}

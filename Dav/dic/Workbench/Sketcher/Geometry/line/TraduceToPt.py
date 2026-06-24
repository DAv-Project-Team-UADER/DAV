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

"""Portuguese spoken-word mapping for the Sketcher line geometry dictionary."""

from .line import line
from .ayuda import ayuda

TraduceToPt = {
    # Comando de ajuda
    "ajuda": ayuda,
    "info": ayuda,
    
    # Criação de linha padrão e sinônimos
    "criar": line['create'],
    "linha": line['create'],
    "criar linha": line['create'],
    "desenhar linha": line['create'],
    "tracar linha": line['create'],
    
    # Criação de linha por pontos e sinônimos
    "linha por pontos": line['create_by_points'],
    "criar linha por pontos": line['create_by_points'],
    "desenhar linha por pontos": line['create_by_points']
}
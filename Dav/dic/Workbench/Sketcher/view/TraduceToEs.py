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

"""Spanish spoken-word mapping for the Sketcher view dictionary."""

from .view import view
from .ayuda import ayuda

TraduceToEs = {
    # Comando de ayuda
    "ayuda": ayuda,
    "info": ayuda,
    
    # Vista de croquis y sinónimos
    "sketch": view['sketch'],
    "vista de croquis": view['sketch'],
    "ver croquis": view['sketch'],
    "orientar croquis": view['sketch'],
    
    # Vista de sección y sinónimos
    "vista de seccion": view['section'],
    "ver seccion": view['section'],
    "recortar vista": view['section'],
    "corte de vista": view['section']
}
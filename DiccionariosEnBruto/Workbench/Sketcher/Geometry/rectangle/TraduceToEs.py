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

"""Spanish spoken-word mapping for the Sketcher rectangle geometry dictionary."""

from .rectangle import rectangle
from .ayuda import ayuda

TraduceToEs = {
    # Comando de ayuda
    "ayuda": ayuda,
    "info": ayuda,
    
    # Creación de rectángulo estándar y sinónimos
    "crear": rectangle['create'],
    "rectangulo": rectangle['create'],
    "cuadro": rectangle['create'],
    "crear rectangulo": rectangle['create'],
    "dibujar rectangulo": rectangle['create'],
    
    # Creación de rectángulo centrado y sinónimos
    "center": rectangle['center'],
    "centro": rectangle['center'],
    "rectangulo centrado": rectangle['center'],
    "crear rectangulo centrado": rectangle['center'],
    "dibujar rectangulo centrado": rectangle['center']
}
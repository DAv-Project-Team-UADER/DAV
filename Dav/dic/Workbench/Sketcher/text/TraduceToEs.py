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

"""Spanish spoken-word mapping for the Sketcher text dictionary."""

from .text import text
from .ayuda import ayuda

TraduceToEs = {
    
    # Texto / Forma de texto y sinónimos
    "crear": text['create'],
    "texto": text['create'],
    "forma de texto": text['create'],
    "crear texto": text['create'],
    "agregar texto": text['create'],
    "dibujar texto": text['create'],

    "ayuda": text['help'],
    "información": text['help'],
    "opciones": text['help'],
}
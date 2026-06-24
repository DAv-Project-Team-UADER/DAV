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

"""Spanish spoken-word mapping for the Sketcher oblong dictionary."""

from .oblong import oblong
from .ayuda import ayuda

TraduceToEs = {
    # Comando de ayuda
    "ayuda": ayuda,
    "info": ayuda,
    
    # Creación de óvalo / ranura y sinónimos
    "crear": oblong['create'],
    "ranura": oblong['create'],
    "ovalo": oblong['create'],
    "colisa": oblong['create'],
    "crear ranura": oblong['create'],
    "dibujar ranura": oblong['create'],
    "crear ovalo": oblong['create'],
    "dibujar ovalo": oblong['create']
}
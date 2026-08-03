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

"""Spanish spoken-word mapping for the Sketcher tools dictionary."""

from .tools import tools
from .ayuda import ayuda

TraduceToEs = {
    
    # Borrar restricciones y sinónimos
    "borrar restricciones": tools['deleteconstraints'],
    "limpiar restricciones": tools['deleteconstraints'],
    "eliminar restricciones": tools['deleteconstraints'],
    
    # Borrar geometría y sinónimos
    "borrar geometria": tools['deletegeometry'],
    "limpiar geometria": tools['deletegeometry'],
    "borrar croquis": tools['deletegeometry'],
    "limpiar croquis": tools['deletegeometry'],
    
    # Fusionar y sinónimos
    "fusionar": tools['merge'],
    "fusionar croquis": tools['merge'],
    "combinar croquis": tools['merge'],
    
    # Reorientar y sinónimos
    "reorientar": tools['reorient'],
    "reorientar croquis": tools['reorient'],
    "cambiar plano del croquis": tools['reorient'],
    
    # Remover alineación de ejes y sinónimos
    "remover ejes": tools['removeaxes'],
    "quitar alineacion de ejes": tools['removeaxes'],

    "ayuda": tools['help'],
    "información": tools['help'],
    "opciones": tools['help']
}
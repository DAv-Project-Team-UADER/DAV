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

"""Spanish spoken-word mapping for the Sketcher line geometry dictionary."""

from .line import line
from .ayuda import ayuda

TraduceToEs = {
    
    # Creación de línea estándar y sinónimos
    "crear": line['create'],
    "linea": line['create'],
    "crear linea": line['create'],
    "dibujar linea": line['create'],
    "trazar linea": line['create'],
    
    # Creación de línea por puntos y sinónimos
    "linea por puntos": line['create_by_points'],
    "crear linea por puntos": line['create_by_points'],
    "dibujar linea por puntos": line['create_by_points'],

    "ayuda": line['help'],
    "informacion": line['help'],
    "opciones": line['help'],
}
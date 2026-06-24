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

"""Spanish spoken-word mapping for the Sketcher external dictionary."""

from .external import external
from .ayuda import ayuda

TraduceToEs = {
    # Comando de ayuda
    "ayuda": ayuda,
    "info": ayuda,
    "informacion": ayuda,
    
    # Comandos de Proyección y sinónimos
    "proyeccion": external['projection'],
    "proyectar": external['projection'],
    "proyectar arista": external['projection'],
    
    # Comandos de Intersección / Geometría Externa y sinónimos
    "interseccion": external['intersection'],
    "intersecar": external['intersection'],
    "geometria externa": external['intersection'],
    "vinculo externo": external['intersection']
}
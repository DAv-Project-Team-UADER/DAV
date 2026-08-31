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

from .Tools import tools
from measure import CreateDimension

TraduceToEs = {
   
    # Cortar de acá
    "medir": lambda: CreateDimension(),
    "medir distancia": lambda: CreateDimension(),
    "acotar": lambda: CreateDimension(),
    "dimensionar": lambda: CreateDimension(),
    "cotar": lambda: CreateDimension(),
    "distancia": lambda: CreateDimension(),
    "medida": lambda: CreateDimension(),
    "longitud": lambda: CreateDimension(),
    "separación": lambda: CreateDimension(),
    "Cota": lambda: CreateDimension(),
    "Acotación": lambda: CreateDimension(),
    "Dimensión": lambda: CreateDimension(),
    "Medida": lambda: CreateDimension(),
     "métrica": lambda: CreateDimension(),
    "Metro": lambda: CreateDimension(),
    "milímetro": lambda: CreateDimension(),
    "centímetro": lambda: CreateDimension(),
    "Cinta": lambda: CreateDimension(),
    "Flexómetro": lambda: CreateDimension(),
    "Metro enrollable": lambda: CreateDimension(),
    "Cinta": lambda: CreateDimension(),
    "regla": lambda: CreateDimension(),
    "Escalímetro": lambda: CreateDimension(),
    "Calibre": lambda: CreateDimension(),
    "Pie de rey": lambda: CreateDimension(),
    "línea de cota": lambda: CreateDimension(),
    "cota lineal": lambda: CreateDimension(),
    "cota": lambda: CreateDimension(),
    "acotación lineal": lambda: CreateDimension(),
    "dimensionado": lambda: CreateDimension(),
    "acotar": lambda: CreateDimension(),
    "micrómetro": lambda: CreateDimension(),
    #HASTA ACA
}
   

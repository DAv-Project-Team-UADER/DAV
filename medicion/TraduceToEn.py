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

TraduceToEn = {
    #CORTAR DE ACA
    "measure": lambda: CreateDimension(),
    "measure distance": lambda: CreateDimension(),
    "distance": lambda: CreateDimension(),
    "Dimension": lambda: CreateDimension(),
    "Dimensioning": lambda: CreateDimension(),
    "Meter": lambda: CreateDimension(),
    "milimeter": lambda: CreateDimension(),
    "centimeter": lambda: CreateDimension(),
    "Tape measure": lambda: CreateDimension(),
    "Tape tool": lambda: CreateDimension(),
    "Tape": lambda: CreateDimension(),
    "Ruler": lambda: CreateDimension(),
    "ruler": lambda: CreateDimension(),
    #HASTA ACA
}
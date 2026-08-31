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

TraduceToPt = {
    #CORTAR DE ACA
    "medir": lambda: CreateDimension(),
    "medida": lambda: CreateDimension(),
    "medir distancia": lambda: CreateDimension(),
    "medir distância": lambda: CreateDimension(),
    "distância": lambda: CreateDimension(),
    "cotar": lambda: CreateDimension(),
    "dimensionar": lambda: CreateDimension(),
    "aferir": lambda: CreateDimension(),
    "mensurar": lambda: CreateDimension(),
    "calcular distância": lambda: CreateDimension(),
    "distância": lambda: CreateDimension(),
    "medida": lambda: CreateDimension(),
    "comprimento": lambda: CreateDimension(),
    "separação": lambda: CreateDimension(),
    "afastamento": lambda: CreateDimension(),
    "extensão": lambda: CreateDimension(),
    "cota": lambda: CreateDimension(),
    "cotagem": lambda: CreateDimension(),
    "acotação": lambda: CreateDimension(),
    "dimensão": lambda: CreateDimension(),
    "métrica": lambda: CreateDimension(),
    "dimensionamento": lambda: CreateDimension(),
    "metro": lambda: CreateDimension(),
    "milímetro": lambda: CreateDimension(),
    "centímetro": lambda: CreateDimension(),
    "flexômetro": lambda: CreateDimension(),
    "metro enrolável": lambda: CreateDimension(),
    "régua": lambda: CreateDimension(),
    "escalímetro": lambda: CreateDimension(),
    "calibre": lambda: CreateDimension(),
    "paquímetro": lambda: CreateDimension(),
    "micrômetro": lambda: CreateDimension(),
    "tolerância": lambda: CreateDimension(),
    "desvio": lambda: CreateDimension(),
    "ajuste": lambda: CreateDimension(),
    "medição": lambda: CreateDimension(),
    "mensuração": lambda: CreateDimension(),
    "aferição": lambda: CreateDimension(),
    "calibração": lambda: CreateDimension(),
    "verificação": lambda: CreateDimension(),
    "inspeção": lambda: CreateDimension(),
    "controle dimensional": lambda: CreateDimension(),
    "metrologia": lambda: CreateDimension(),
   # HASTA ACA
}
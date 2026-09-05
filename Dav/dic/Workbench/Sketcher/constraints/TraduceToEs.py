# Copyright (C) 2026 El Equipo del Proyecto DAV
# Copyright (C) 2026 The DAV Project Team
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

"""Spanish spoken-word mapping for the constraints dictionary."""

from .constraints import constraints

TraduceToEs = {
    'dimensión': constraints['dimension'],
    'cota': constraints['dimension'],
    'cota horizontal': constraints['horizontal'],
    'distancia horizontal': constraints['horizontal'],
    'cota vertical': constraints['vertical'],
    'distancia vertical': constraints['vertical'],
    'cota angular': constraints['angle'],
    'ángulo': constraints['angle'],
    'radio': constraints['radius'],
    'cota radial': constraints['radius'],
    'diámetro': constraints['diameter'],
    'cota diametral': constraints['diameter'],
    'distancia': constraints['distance'],
    'cota de distancia': constraints['distance'],
    'geométricas': constraints['geometric'],
    'geométrica': constraints['geometric'],
    'restricciones geométricas': constraints['geometric'],
    'restricciones de geometría': constraints['geometric'],
    'ayuda': constraints['help'],
    'información': constraints['help'],
    'opciones': constraints['help'],
    'longitud': constraints['dimension'],
    'horizontal': constraints['horizontal'],
    'vertical': constraints['vertical'],
    'cota automática': constraints['radiam'],
    'cota radio diámetro': constraints['radiam'],
    'radio o diámetro': constraints['radiam'],
}

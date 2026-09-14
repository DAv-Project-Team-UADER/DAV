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

"""Portuguese spoken-word mapping for the circle dictionary."""

from .circle import circle

TraduceToPt = {
    'criar':                circle['create'],
    'círculo':              circle['create'],
    'centro':               circle['create'],
    'círculo pelo centro':  circle['create'],

    'três pontos':          circle['3point'],
    'círculo três pontos':  circle['3point'],
    '3 pontos':             circle['3point'],

    'ajuda':                circle['help'],
    'informação':             circle['help'],
    'opções':               circle['help'],

    # Círculo por coordenadas ditadas
    "circulo por centro": circle['create_by_center'],
    "criar circulo por centro": circle['create_by_center'],
    "circulo por raio": circle['create_by_center'],
    "circulo por coordenadas": circle['create_by_center'],

    # Círculo por 3 pontos — novo paramétrico com 6 floats + label opcional
    "circulo por tres pontos": circle['create_by_3_points'],
    "círculo por três pontos": circle['create_by_3_points'],
    "criar circulo por tres pontos": circle['create_by_3_points'],
    "criar círculo por três pontos": circle['create_by_3_points'],
    "circulo por 3 pontos": circle['create_by_3_points'],
}

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

"""Spanish spoken-word mapping for the circle dictionary."""

from .circle import circle

TraduceToEs = {
    'crear círculo': circle['create'],
    'círculo': circle['create'],
    'centro': circle['create'],
    'círculo desde centro': circle['create'],
    'círculo por parámetros': circle['create_by_center_radius'],
    'círculo por centro y radio': circle['create_by_center_radius'],
    'crear círculo con parámetros': circle['create_by_center_radius'],
    'círculo por tres puntos paramétrico': circle['create_by_3points'],
    'tres puntos paramétrico': circle['create_by_3points'],

    'tres puntos': circle['3point'],
    'círculo tres puntos': circle['3point'],
    '3 puntos': circle['3point'],

    'ayuda':                circle['help'],
    'informacion':             circle['help'],
    'opciones':             circle['help'],

    # Círculo por coordenadas dictadas (ventana por voz, como línea por puntos)
    "circulo por centro": circle['create_by_center'],
    "crear circulo por centro": circle['create_by_center'],
    "circulo por radio": circle['create_by_center'],
    "circulo por coordenadas": circle['create_by_center'],

    # Círculo por 3 puntos — nuevo paramétrico con 6 floats + label opcional
    "circulo por tres puntos": circle['create_by_3_points'],
    "círculo por tres puntos": circle['create_by_3_points'],
    "crear circulo por tres puntos": circle['create_by_3_points'],
    "crear círculo por tres puntos": circle['create_by_3_points'],
    "circulo tres puntos por coordenadas": circle['create_by_3_points'],
}

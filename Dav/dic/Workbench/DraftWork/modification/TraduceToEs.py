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

from .modification import modification

TraduceToEs = {
    'escalar': modification['scale'],
    'redimensionar': modification['scale'],

    'vista_2d': modification['shape_2d_view'],
    'proyeccion_2d': modification['shape_2d_view'],

    'pendiente': modification['slope'],
    'inclinacion': modification['slope'],

    'dividir': modification['split'],
    'separar': modification['split'],

    'estirar': modification['stretch'],
    'extender': modification['stretch'],

    'resaltar_subelemento': modification['subelement_highlight'],
    'resaltar': modification['subelement_highlight'],

    'recortar': modification['trimex'],
    'ajustar': modification['trimex'],

    'mejorar': modification['upgrade'],
    'actualizar': modification['upgrade'],

    'cable_a_bspline': modification['wire_to_bspline'],
    'bspline': modification['wire_to_bspline'],

    'help': modification['help'],
    'ayuda': modification['help'],
    'opciones': modification['help'],
}
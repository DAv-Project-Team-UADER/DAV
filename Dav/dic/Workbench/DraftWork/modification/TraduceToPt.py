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

TraduceToPt = {
    'escalar': modification['scale'],
    'redimensionar': modification['scale'],

    'vista': modification['shape_2d_view'],
    "visualização": modification['shape_2d_view'],
    'projeção': modification['shape_2d_view'],

    'inclinação': modification['slope'],
    'declive': modification['slope'],

    'dividir': modification['split'],
    'separar': modification['split'],

    'esticar': modification['stretch'],
    'extender': modification['stretch'],

    'destacar_subelemento': modification['subelement_highlight'],
    'destacar': modification['subelement_highlight'],

    'aparar': modification['trimex'],
    'ajustar': modification['trimex'],

    'melhorar': modification['upgrade'],
    'atualizar': modification['upgrade'],

    'fio_para_bspline': modification['wire_to_bspline'],
    'bspline': modification['wire_to_bspline'],

    'help': modification['help'],
    'ajuda': modification['help'],
    'opções': modification['help'],
}
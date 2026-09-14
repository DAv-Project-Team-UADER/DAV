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

# ============================================================
# English translations – Sketcher Polygon
# ============================================================

from .polygon import polygon

TraduceToEn = {
    # Main commands
    "pentagon": polygon["pentagon"],
    "octagon": polygon["octagon"],
    "regular": polygon["regular"],
    "regular pentagon": polygon["pentagon"],
    "regular octagon": polygon["octagon"],
    "polygon": polygon["regular"],
    "regular polygon": polygon["regular"],
    "create pentagon": polygon["pentagon"],
    "create octagon": polygon["octagon"],
    "five sides": polygon["pentagon"],
    "eight sides": polygon["octagon"],

    "help": polygon["help"],
    "info": polygon["help"],
    "options": polygon["help"],

    # Regular polygon by dictated coordinates
    "polygon by sides": polygon['create_regular'],
    "create polygon by sides": polygon['create_regular'],
    "regular polygon by sides": polygon['create_regular'],
    "polygon by coordinates": polygon['create_regular'],

    # Regular polygon by dictated parameters
    "polygon by parameters": polygon['create_regular_polygon'],
    "polygon with sides": polygon['create_regular_polygon'],
    "create polygon by parameters": polygon['create_regular_polygon'],
}

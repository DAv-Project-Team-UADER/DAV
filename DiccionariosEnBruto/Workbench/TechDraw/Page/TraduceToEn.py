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

from .page import page
from .ayuda import ayuda

TraduceToEn = {

    # Default Page
    "default page": page["default"],
    "new page": page["default"],
    "create page": page["default"],

    # Template Page
    "template page": page["template"],
    "page template": page["template"],
    "new template page": page["template"],

    # Redraw
    "redraw page": page["redraw"],
    "refresh page": page["redraw"],
    "update page": page["redraw"],

    # Print
    "print": page["print"],
    "print page": page["print"],
    "print all": page["print"],

    # Export DXF
    "export dxf": page["dxf"],
    "dxf": page["dxf"],
    "drawing exchange format": page["dxf"],
    "save dxf": page["dxf"],
    "export drawing exchange format": page["dxf"],
    "save drawing exchange format": page["dxf"],

    # Export SVG
    "export svg": page["svg"],
    "svg": page["svg"],
    "save svg": page["svg"],
    "export svg format": page["svg"],
    "save svg format": page["svg"],
    "svg format": page["svg"],
    "scalable vector graphics": page["svg"],
    "export scalable vector graphics": page["svg"],
    "save scalable vector graphics": page["svg"],

    "help": ayuda,
}

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
# English translations – StdViews DrawStyles
# ============================================================

from .drawstyles import drawstyles

TraduceToEn = {
    # Main styles
    "asis": drawstyles["styleasis"],
    "flat": drawstyles["flatlines"],
    "hidden": drawstyles["hiddenline"],
    "noshading": drawstyles["noshading"],
    "points": drawstyles["points"],
    "shaded": drawstyles["shaded"],
    "wireframe": drawstyles["wireframe"],
    "help": drawstyles["help"],

    # Synonyms
    "as is": drawstyles["styleasis"],
    "original": drawstyles["styleasis"],

    "flat lines": drawstyles["flatlines"],
    "flatlines": drawstyles["flatlines"],

    "hidden line": drawstyles["hiddenline"],
    "hidden lines": drawstyles["hiddenline"],

    "no shading": drawstyles["noshading"],
    "without shading": drawstyles["noshading"],

    "point mode": drawstyles["points"],
    "dots": drawstyles["points"],

    "shaded view": drawstyles["shaded"],
    "solid": drawstyles["shaded"],

    "wire": drawstyles["wireframe"],
    "wire frame": drawstyles["wireframe"],
}

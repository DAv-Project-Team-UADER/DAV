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
# English translations – Sketcher Ellipse
# ============================================================

from .ellipse import ellipse

TraduceToEn = {
    # Main commands
    "center": ellipse["center"],
    "3points": ellipse["3points"],
    "elliptic": ellipse["elliptic"],
    "hyperbolic": ellipse["hyperbolic"],
    "parabolic": ellipse["parabolic"],
    "help": ellipse["help"],

    # Aliases
    "ellipse center": ellipse["center"],
    "ellipse 3 points": ellipse["3points"],
    "ellipse arc": ellipse["elliptic"],
    "hyperbola arc": ellipse["hyperbolic"],
    "parabola arc": ellipse["parabolic"],
}

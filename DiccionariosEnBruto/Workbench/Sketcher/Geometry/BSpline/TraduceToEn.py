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
# English translations – Sketcher BSpline
# ============================================================

# SPDX-License-Identifier: GPL-3.0-or-later

from .bspline import bspline

TraduceToEn = {
    # Main commands
    "create": bspline["create"],
    "interpolation": bspline["interpolation"],
    "periodic": bspline["periodic"],
    "periodicinterp": bspline["periodicinterp"],

    # Aliases / synonyms
    "create bspline": bspline["create"],
    "create b-spline": bspline["create"],
    "bspline curve": bspline["create"],
    "b-spline curve": bspline["create"],
    "spline curve": bspline["create"],

    "interpolated": bspline["interpolation"],
    "interpolated bspline": bspline["interpolation"],

    "periodic bspline": bspline["periodic"],
    "closed bspline": bspline["periodic"],

    "help": bspline["help"],
    "info": bspline["help"],
    "options": bspline["help"],

}

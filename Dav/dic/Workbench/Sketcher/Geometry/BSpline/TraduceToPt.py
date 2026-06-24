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
# Portuguese translations – Sketcher BSpline
# ============================================================

from .bspline import bspline

TraduceToPt = {
    # Comandos principais
    "criar": bspline["create"],
    "interpolacao": bspline["interpolation"],
    "periodica": bspline["periodic"],
    "interpolacao periodica": bspline["periodicinterp"],
    "ajuda": bspline["help"],

    # Sinônimos
    "criar bspline": bspline["create"],
    "criar b-spline": bspline["create"],
    "curva bspline": bspline["create"],
    "curva b-spline": bspline["create"],
    "curva spline": bspline["create"],

    "interpolada": bspline["interpolation"],
    "bspline interpolada": bspline["interpolation"],

    "bspline periodica": bspline["periodic"],
    "bspline fechada": bspline["periodic"],
}

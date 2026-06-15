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

"""English spoken-word mapping for the Curve dictionary."""

from .curve import curve

TraduceToEn = {
    # Draft BezCurve
    "bezier":              curve['bezier'],
    "bezier curve":        curve['bezier'],
    "n degree bezier":     curve['bezier'],

    # Draft BSpline
    "bspline":             curve['bspline'],
    "b spline":            curve['bspline'],
    "spline":              curve['bspline'],
    "smooth curve":        curve['bspline'],

    # Draft CubicBezCurve
    "cubic":               curve['cubic'],
    "cubic bezier":        curve['cubic'],
    "cubic curve":         curve['cubic'],
    "third degree bezier": curve['cubic'],

    "help":                curve['help'],
    "info":                curve['help'],
    "options":             curve['help']
}
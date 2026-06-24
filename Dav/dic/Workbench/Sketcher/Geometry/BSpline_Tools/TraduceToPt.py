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
# Portuguese translations – Sketcher BSpline Tools
# ============================================================

from .bspline_tools import bspline_tools

TraduceToPt = {
    # Comandos principais
    "para nurbs": bspline_tools["tonurbs"],
    "diminuir grau": bspline_tools["decrease"],
    "aumentar grau": bspline_tools["increase"],
    "nó": bspline_tools["knot"],
    "unir": bspline_tools["join"],
    "ajuda": bspline_tools["help"],

    # Sinônimos
    "converter para nurbs": bspline_tools["tonurbs"],
    "baixar grau": bspline_tools["decrease"],
    "subir grau": bspline_tools["increase"],
    "inserir nó": bspline_tools["knot"],
    "unir curva": bspline_tools["join"],
}

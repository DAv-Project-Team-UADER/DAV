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
# Portuguese translations – Sketcher Ellipse
# ============================================================

from ._ellipse import ellipse

TraduceToPt = {
    # Comandos principais
    "centro": ellipse["center"],
    "3 pontos": ellipse["3points"],
    "eliptica": ellipse["elliptic"],
    "hiperbolica": ellipse["hyperbolic"],
    "parabolica": ellipse["parabolic"],

    # Sinônimos
    "elipse centro": ellipse["center"],
    "elipse 3 pontos": ellipse["3points"],
    "arco eliptico": ellipse["elliptic"],
    "arco hiperbolico": ellipse["hyperbolic"],
    "arco parabolico": ellipse["parabolic"],

    "ajuda": ellipse["help"],
    "informação": ellipse["help"],
    "opções": ellipse["help"],

    # Elipse por coordenadas ditadas
    "elipse por centro": ellipse['create_by_center'],
    "criar elipse por centro": ellipse['create_by_center'],
    "elipse por raios": ellipse['create_by_center'],
    "elipse por coordenadas": ellipse['create_by_center'],
}

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
# Spanish translations – Sketcher Ellipse
# ============================================================

from ._ellipse import ellipse

TraduceToEs = {
    # Comandos principales (ahora paramétricos con ventana) — dígito + palabra para Vosk
    "centro": ellipse["center"],
    "3 puntos": ellipse["3points"],
    "tres puntos": ellipse["3points"],
    "tres punto": ellipse["3points"],
    "eliptica": ellipse["elliptic"],
    "elíptica": ellipse["elliptic"],
    "hiperbolica": ellipse["hyperbolic"],
    "hiperbólica": ellipse["hyperbolic"],
    "parabolica": ellipse["parabolic"],
    "parabólica": ellipse["parabolic"],

    # Sinónimos
    "elipse centro": ellipse["center"],
    "elipse 3 puntos": ellipse["3points"],
    "elipse tres puntos": ellipse["3points"],
    "arco eliptico": ellipse["elliptic"],
    "arco elíptico": ellipse["elliptic"],
    "arco elipse": ellipse["elliptic"],
    "elipse arco": ellipse["elliptic"],
    "arco hiperbolico": ellipse["hyperbolic"],
    "arco hiperbólico": ellipse["hyperbolic"],
    "arco hiperbola": ellipse["hyperbolic"],
    "hiperbola": ellipse["hyperbolic"],
    "arco parabolico": ellipse["parabolic"],
    "arco parabólico": ellipse["parabolic"],
    "arco parabola": ellipse["parabolic"],
    "parabola": ellipse["parabolic"],
    "parábola": ellipse["parabolic"],

    "ayuda": ellipse["help"],
    "informacion": ellipse["help"],
    "opciones": ellipse["help"],

    # Elipse por coordenadas dictadas (ventana como línea por puntos)
    "elipse por centro": ellipse['create_by_center'],
    "crear elipse por centro": ellipse['create_by_center'],
    "elipse por radios": ellipse['create_by_center'],
    "elipse por coordenadas": ellipse['create_by_center'],

    # Nuevos alias explícitos para los 4 modos paramétricos
    "elipse por tres puntos": ellipse['create_by_3_points'],
    "crear elipse por tres puntos": ellipse['create_by_3_points'],
    "elipse por 3 puntos": ellipse['create_by_3_points'],
    "arco eliptico por coordenadas": ellipse['create_elliptic'],
    "elipse arco eliptico": ellipse['create_elliptic'],
    "arco hiperbolico por coordenadas": ellipse['create_hyperbolic'],
    "arco hiperbólico por coordenadas": ellipse['create_hyperbolic'],
    "arco parabolico por coordenadas": ellipse['create_parabolic'],
    "arco parabólico por coordenadas": ellipse['create_parabolic'],
}

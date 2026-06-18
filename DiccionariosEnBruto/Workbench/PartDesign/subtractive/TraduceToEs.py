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

from .subtractive import subtractive
from .ayuda import ayuda

TraduceToEs = {
    # Pocket
    "vaciado": subtractive["pocket"],
    "corte": subtractive["pocket"],

    # Groove
    "ranura": subtractive["groove"],
    "canal": subtractive["groove"],

    # Hole
    "agujero": subtractive["hole"],
    "orificio": subtractive["hole"],

    # Subtractive Box
    "cajasustractiva": subtractive["subtractivebox"],

    # Subtractive Cone
    "conosustractivo": subtractive["subtractivecone"],

    # Subtractive Cylinder
    "cilindrosustractivo": subtractive["subtractivecylinder"],

    # Subtractive Ellipsoid
    "elipsoidesustractivo": subtractive["subtractiveellipsoid"],

    # Subtractive Helix
    "helicesustractiva": subtractive["subtractivehelix"],

    # Subtractive Loft
    "recubrimientosustractivo": subtractive["subtractiveloft"],

    # Subtractive Pipe
    "tuberiasustractiva": subtractive["subtractivepipe"],

    # Subtractive Prism
    "prismasustractivo": subtractive["subtractiveprism"],

    # Subtractive Sphere
    "esferasustractiva": subtractive["subtractivesphere"],

    # Subtractive Torus
    "torosustractivo": subtractive["subtractivetorus"],

    # Subtractive Wedge
    "cunasustractiva": subtractive["subtractivewedge"],

    # Boolean
    "booleano": subtractive["boolean"],
    "operacionbooleana": subtractive["boolean"],

    # Help
    "ayuda": ayuda,
    "manual": ayuda,
    "soporte": ayuda,
    "documentacion": ayuda,
}

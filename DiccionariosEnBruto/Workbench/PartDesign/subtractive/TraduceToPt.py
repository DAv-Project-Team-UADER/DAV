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

"""Portuguese spoken-word mapping for PartDesign subtractive commands."""

from .subtractive import subtractive
from .ayuda import ayuda

TraduceToPt = {
    # Pocket
    "bolso": subtractive["pocket"],
    "corte": subtractive["pocket"],

    # Groove
    "ranhura": subtractive["groove"],
    "canal": subtractive["groove"],

    # Hole
    "furo": subtractive["hole"],
    "perfuração": subtractive["hole"],

    # Subtractive Box
    "caixasubtrativa": subtractive["subtractivebox"],
    "cortecaixa": subtractive["subtractivebox"],

    # Subtractive Cone
    "conesubtrativo": subtractive["subtractivecone"],
    "cortecone": subtractive["subtractivecone"],

    # Subtractive Cylinder
    "cilindrosubtrativo": subtractive["subtractivecylinder"],
    "cortecilindro": subtractive["subtractivecylinder"],

    # Subtractive Ellipsoid
    "elipsoidesubtrativo": subtractive["subtractiveellipsoid"],
    "corteelipsoide": subtractive["subtractiveellipsoid"],

    # Subtractive Helix
    "helicesubtrativa": subtractive["subtractivehelix"],
    "cortehelice": subtractive["subtractivehelix"],

    # Subtractive Loft
    "loftsubtrativo": subtractive["subtractiveloft"],
    "corteloft": subtractive["subtractiveloft"],

    # Subtractive Pipe
    "tubosubtrativo": subtractive["subtractivepipe"],
    "cortetubo": subtractive["subtractivepipe"],

    # Subtractive Prism
    "prismasubtrativo": subtractive["subtractiveprism"],
    "corteprisma": subtractive["subtractiveprism"],

    # Subtractive Sphere
    "esferasubtrativa": subtractive["subtractivesphere"],
    "corteesfera": subtractive["subtractivesphere"],

    # Subtractive Torus
    "torosubtrativo": subtractive["subtractivetorus"],
    "cortetoro": subtractive["subtractivetorus"],

    # Subtractive Wedge
    "cunhasubtrativa": subtractive["subtractivewedge"],
    "cortecunha": subtractive["subtractivewedge"],

    # Boolean
    "booleano": subtractive["boolean"],
    "operaçãobooleana": subtractive["boolean"],
    "opbooleana": subtractive["boolean"],

    # Help
    "ajuda": ayuda,
    "manual": ayuda,
    "suporte": ayuda,
    "documentação": ayuda,
}

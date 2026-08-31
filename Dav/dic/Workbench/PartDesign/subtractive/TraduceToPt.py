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
    "caixa sustractiva": subtractive["subtractivebox"],
    "corte caixa": subtractive["subtractivebox"],

    # Subtractive Cone
    "cono sustractivo": subtractive["subtractivecone"],
    "corte cono": subtractive["subtractivecone"],

    # Subtractive Cylinder
    "cilindro sustractivo": subtractive["subtractivecylinder"],
    "corte cilindro": subtractive["subtractivecylinder"],

    # Subtractive Ellipsoid
    "elipsoide sustractivo": subtractive["subtractiveellipsoid"],
    "corte elipsoide": subtractive["subtractiveellipsoid"],

    # Subtractive Helix
    "helice subtrativa": subtractive["subtractivehelix"],
    "corte helice": subtractive["subtractivehelix"],

    # Subtractive Loft
    "loft sustractivo": subtractive["subtractiveloft"],
    "corte loft": subtractive["subtractiveloft"],

    # Subtractive Pipe
    "tubo sustractivo": subtractive["subtractivepipe"],
    "corte tubo": subtractive["subtractivepipe"],

    # Subtractive Prism
    "prisma sustractivo": subtractive["subtractiveprism"],
    "corte prisma": subtractive["subtractiveprism"],

    # Subtractive Sphere
    "esfera sustractiva": subtractive["subtractivesphere"],
    "corte esfera": subtractive["subtractivesphere"],

    # Subtractive Torus
    "toro sustractivo": subtractive["subtractivetorus"],
    "corte toro": subtractive["subtractivetorus"],

    # Subtractive Wedge
    "cuna sustractiva": subtractive["subtractivewedge"],
    "corte cuna": subtractive["subtractivewedge"],

    # Boolean
    "booleano": subtractive["boolean"],
    "operação booleana": subtractive["boolean"],

    # Cortes por medida ditada (sem dialogo)
    "vazio por medida":      subtractive["pocket_by_length"],
    "esvaziar por medida":   subtractive["pocket_by_length"],

    "furo por medidas":      subtractive["hole_by_size"],
    "perfurar por medidas":  subtractive["hole_by_size"],

    "ranhura por angulo":    subtractive["groove_by_angle"],

    # Help
    "ajuda": subtractive['help'],
    "informação": subtractive['help'],
    "opções": subtractive['help'],
}

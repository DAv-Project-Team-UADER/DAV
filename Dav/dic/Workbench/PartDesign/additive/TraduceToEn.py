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
import additive as additive
import ayuda as ayuda

TraduceToEn = {
    # Pad
    "pad": additive["pad"],
    "pad feature": additive["pad"],

    # Revolution
    "revolution": additive["revolution"],
    "revolution feature": additive["revolution"],

    # AdditiveHelix
    "additive helix": additive["additivehelix"],
    "Coil feature": additive["additivehelix"],

    # AdditiveLoft
    "additive loft": additive["additiveloft"],
    "loft feature": additive["additiveloft"],

    # AdditivePipe
    "additive pipe": additive["additivepipe"],
    "pipe feature": additive["additivepipe"],

    # AdditiveBox
    "additive box": additive["additivebox"],
    "Additive solid box": additive["additivebox"],

    # AdditiveCone
    "additive cone": additive["additivecone"],
    "cone feature": additive["additivecone"],

    # AdditiveCylinder
    "additive cylinder": additive["additivecylinder"],
    "cylinder feature": additive["additivecylinder"],

    # AdditiveEllipsoid
    "additive ellipsoid": additive["additiveellipsoid"],
    "ellipsoid feature": additive["additiveellipsoid"],

    # AdditivePrism
    "additive prism": additive["additiveprism"],
    "prism feature": additive["additiveprism"],

    # AdditiveSphere
    "additive sphere": additive["additivesphere"],
    "sphere feature": additive["additivesphere"],

    # AdditiveTorus
    "additive torus": additive["additivetorus"],
    "torus feature": additive["additivetorus"],
    
    # AdditiveWedge
    "additive wedge": additive["additivewedge"],
    "wedge feature": additive["additivewedge"],
    
    # pad_sketch
    "extrude sketch": additive["pad_sketch"],
    "extend profile": additive["pad_sketch"],
    "thicken drawing": additive["pad_sketch"],

    # loft_profiles
    "blend shapes": additive["loft_profiles"],
    "sweep surfaces": additive["loft_profiles"],
    "morph sections": additive["loft_profiles"],


    "help":            additive['help'],
    "info":            additive['help'],
    "options":         additive['help']
}

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

traduceToEn = {
    "pad": additive["pad"],
    "pad feature": additive["pad"],
    "revolution": additive["revolution"],
    "revolution feature": additive["revolution"],
    "additive helix": additive["additivehelix"],
    "Coil feature": additive["additivehelix"],
    "additive loft": additive["additiveloft"],
    "loft feature": additive["additiveloft"],
    "additive pipe": additive["additivepipe"],
    "pipe feature": additive["additivepipe"],
    "additive box": additive["additivebox"],
    "Additive solid box": additive["additivebox"],
    "additive cone": additive["additivecone"],
    "cone feature": additive["additivecone"],
    "additive cylinder": additive["additivecylinder"],
    "cylinder feature": additive["additivecylinder"],
    "additive ellipsoid": additive["additiveellipsoid"],
    "ellipsoid feature": additive["additiveellipsoid"],
    "additive prism": additive["additiveprism"],
    "prism feature": additive["additiveprism"],
    "additive sphere": additive["additivesphere"],
    "sphere feature": additive["additivesphere"],
    "additive torus": additive["additivetorus"],
    "torus feature": additive["additivetorus"],
    "additive wedge": additive["additivewedge"],
    "wedge feature": additive["additivewedge"],
    "help": ayuda,
}

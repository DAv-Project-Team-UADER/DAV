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

TraduceToPt = {
    #Ressalto
    'ressalto':         additive['pad'],

    #Revolução
    'revolucao':        additive['revolution'],

    #Hélice aditiva
    'heliceaditiva':     additive['additivehelix'],

    #Loft aditivo
    'loftaditivo':      additive['additiveloft'],
    'Transição aditiva':      additive['additiveloft'],
    'Ressalto por loft':      additive['additiveloft'],

    #Tubo aditivo
    'tuboaditivo':      additive['additivepipe'],
    'varrimento aditivo':      additive['additivepipe'],
    'resaltopor varrimento':      additive['additivepipe'],

    #Caixa aditiva
    'caixaaditiva':     additive['additivebox'],
    'paralelepipado aditivo':     additive['additivebox'],
    'bloco aditivo':     additive['additivebox'],

    #Cone aditivo
    'cone aditivo':      additive['additivecone'],
    'conical aditivo':      additive['additivecone'],
    
    #Cilindro aditivo
    'cilindro aditivo':  additive['additivecylinder'],

    #Elipsoide aditivo
    'elipsoide aditivo': additive['additiveellipsoid'],
    'esferoide aditivo': additive['additiveellipsoid'],
    'ovoide aditivo': additive['additiveellipsoid'],

    #Prisma aditivo
    'prisma aditivo':     additive['additiveprism'],
    'prisma triangular aditivo':     additive['additiveprism'],
    'prisma quadrangular aditivo':     additive['additiveprism'],

    #Esfera aditiva
    'esfera aditiva':    additive['additivesphere'],
    'globo aditivo':    additive['additivesphere'],
    'bola aditiva':    additive['additivesphere'],

    #Toro aditivo
    'toro aditivo':     additive['additivetorus'],
    'rosca aditiva':     additive['additivetorus'],
    'anel aditivo':     additive['additivetorus'],

    #Cunha aditiva
    'cunha aditiva':     additive['additivewedge'],
    'wedge aditivo':     additive['additivewedge'],
    'chanfro aditivo':     additive['additivewedge'],

    'help':              additive['help'],
}

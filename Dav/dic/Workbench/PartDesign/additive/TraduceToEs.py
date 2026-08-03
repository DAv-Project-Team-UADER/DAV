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

TraduceToEs = {
    # Rellenar
    "Rellenar":         additive["pad"],
    "Relleno":          additive["pad"],
    "Rellenar con":     additive["pad"],
    "Rellenar a":       additive["pad"],
    "Rellenar hasta":   additive["pad"],

    # Transformacion
    "Transformación":   additive["revolution"],
    "Transformar":      additive["revolution"],
    "Transformar con":  additive["revolution"],
    "Transformar a":    additive["revolution"],
    "Transformar hasta":additive["revolution"],

    #Helice Aditiva
    "Hélice Aditiva":   additive["additivehelix"],
    "Hélice":           additive["additivehelix"],
    "Crear Hélice":     additive["additivehelix"],
    "Crear Hélice con": additive["additivehelix"],
    "Crear Hélice a":   additive["additivehelix"],
    "Crear Hélice hasta":additive["additivehelix"],

    #Sombreado aditivo
    "Sombreado Aditivo":   additive["additiveloft"],
    "Sombreado":           additive["additiveloft"],
    "Crear Sombreado":     additive["additiveloft"],
    "Crear Sombreado con": additive["additiveloft"],
    "Crear Sombreado a":   additive["additiveloft"],
    "Crear Sombreado hasta":additive["additiveloft"],

    #Tubo aditivo
    "Tubo Aditivo":   additive["additivepipe"],
    "Tubo":           additive["additivepipe"],
    "Crear Tubo":     additive["additivepipe"],
    "Crear Tubo con": additive["additivepipe"],
    "Crear Tubo a":   additive["additivepipe"],
    "Crear Tubo hasta":additive["additivepipe"],

    #Caja aditiva
    "Caja Aditiva":   additive["additivebox"],
    "Caja":           additive["additivebox"],
    "Crear Caja":     additive["additivebox"],
    "Crear Caja con": additive["additivebox"],
    "Crear Caja a":   additive["additivebox"],
    "Crear Caja hasta":additive["additivebox"],

    #Cono aditivo
    "Cono Aditivo":   additive["additivecone"],
    "Cono":           additive["additivecone"],
    "Crear Cono":     additive["additivecone"],
    "Crear Cono con": additive["additivecone"],
    "Crear Cono a":   additive["additivecone"],
    "Crear Cono hasta":additive["additivecone"],

    #Cilindro aditivo
    "Cilindro Aditivo":   additive["additivecylinder"],
    "Cilindro":           additive["additivecylinder"],
    "Crear Cilindro":     additive["additivecylinder"],
    "Crear Cilindro con": additive["additivecylinder"],
    "Crear Cilindro a":   additive["additivecylinder"],
    "Crear Cilindro hasta":additive["additivecylinder"],

    #Elipsoide aditivo
    "Elipsoide Aditivo":   additive["additiveellipsoid"],
    "Elipse estirada":           additive["additiveellipsoid"],
    "Crear Elipse estirada":     additive["additiveellipsoid"],
    "Crear Elipse estirada con": additive["additiveellipsoid"],
    "Crear Elipse estirada a":   additive["additiveellipsoid"],
    "Crear Elipse estirada hasta":additive["additiveellipsoid"],

    #Prisma aditivo
    "Prisma Aditivo":   additive["additiveprism"],
    "Prisma":           additive["additiveprism"],
    "Crear Prisma":     additive["additiveprism"],
    "Crear Prisma con": additive["additiveprism"],
    "Crear Prisma a":   additive["additiveprism"],
    "Crear Prisma hasta":additive["additiveprism"],

    #Esfera aditiva
    "Esfera Aditiva":   additive["additivesphere"],
    "Esfera":           additive["additivesphere"],
    "Crear Esfera":     additive["additivesphere"],
    "Crear Esfera con": additive["additivesphere"],
    "Crear Esfera a":   additive["additivesphere"],
    "Crear Esfera hasta":additive["additivesphere"],

    #Toro aditivo
    "Toro Aditivo":   additive["additivetorus"],
    "Toro":           additive["additivetorus"],
    "Crear Toro":     additive["additivetorus"],
    "Crear Toro con": additive["additivetorus"],
    "Crear Toro a":   additive["additivetorus"],
    "Crear Toro hasta":additive["additivetorus"],

    #Cuña aditiva
    "Cuña Aditiva":   additive["additivewedge"],
    "Cuña":           additive["additivewedge"],
    "Crear Cuña":     additive["additivewedge"],
    "Crear Cuña con": additive["additivewedge"],
    "Crear Cuña a":   additive["additivewedge"],
    "Crear Cuña hasta":additive["additivewedge"],
    
    # pad_sketch
    "extruir boceto": additive["pad_sketch"],
    "extender perfil": additive["pad_sketch"],
    "engrosar dibujo": additive["pad_sketch"],

    # loft_profiles
    "mezclar formas": additive["loft_profiles"],
    "barrer superficies": additive["loft_profiles"],
    "deformar secciones": additive["loft_profiles"],

    #Ayuda
    "ayuda":                additive["help"],
    "información":          additive["help"],
    "opciones":             additive["help"]
}

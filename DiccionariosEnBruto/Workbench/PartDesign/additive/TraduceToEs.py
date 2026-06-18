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
    "Helice Aditiva":   additive["helix"],
    "Helice":           additive["helix"],
    "Crear Helice":     additive["helix"],
    "Crear Helice con": additive["helix"],
    "Crear Helice a":   additive["helix"],
    "Crear Helice hasta":additive["helix"],

    #Sombreado aditivo
    "Sombreado Aditivo":   additive["loft"],
    "Sombreado":           additive["loft"],
    "Crear Sombreado":     additive["loft"],
    "Crear Sombreado con": additive["loft"],
    "Crear Sombreado a":   additive["loft"],
    "Crear Sombreado hasta":additive["loft"],

    #Tubo aditivo
    "Tubo Aditivo":   additive["pipe"],
    "Tubo":           additive["pipe"],
    "Crear Tubo":     additive["pipe"],
    "Crear Tubo con": additive["pipe"],
    "Crear Tubo a":   additive["pipe"],
    "Crear Tubo hasta":additive["pipe"],

    #Caja aditiva
    "Caja Aditiva":   additive["box"],
    "Caja":           additive["box"],
    "Crear Caja":     additive["box"],
    "Crear Caja con": additive["box"],
    "Crear Caja a":   additive["box"],
    "Crear Caja hasta":additive["box"],

    #Cono aditivo
    "Cono Aditivo":   additive["cone"],
    "Cono":           additive["cone"],
    "Crear Cono":     additive["cone"],
    "Crear Cono con": additive["cone"],
    "Crear Cono a":   additive["cone"],
    "Crear Cono hasta":additive["cone"],

    #Cilindro aditivo
    "Cilindro Aditivo":   additive["cylinder"],
    "Cilindro":           additive["cylinder"],
    "Crear Cilindro":     additive["cylinder"],
    "Crear Cilindro con": additive["cylinder"],
    "Crear Cilindro a":   additive["cylinder"],
    "Crear Cilindro hasta":additive["cylinder"],

    #Elipsoide aditivo
    "Elipsoide Aditivo":   additive["ellipsoid"],
    "Elipse estirada":           additive["ellipsoid"],
    "Crear Elipse estirada":     additive["ellipsoid"],
    "Crear Elipse estirada con": additive["ellipsoid"],
    "Crear Elipse estirada a":   additive["ellipsoid"],
    "Crear Elipse estirada hasta":additive["ellipsoid"],

    #Prisma aditivo
    "Prisma Aditivo":   additive["prism"],
    "Prisma":           additive["prism"],
    "Crear Prisma":     additive["prism"],
    "Crear Prisma con": additive["prism"],
    "Crear Prisma a":   additive["prism"],
    "Crear Prisma hasta":additive["prism"],

    #Esfera aditiva
    "Esfera Aditiva":   additive["sphere"],
    "Esfera":           additive["sphere"],
    "Crear Esfera":     additive["sphere"],
    "Crear Esfera con": additive["sphere"],
    "Crear Esfera a":   additive["sphere"],
    "Crear Esfera hasta":additive["sphere"],

    #Toro aditivo
    "Toro Aditivo":   additive["torus"],
    "Toro":           additive["torus"],
    "Crear Toro":     additive["torus"],
    "Crear Toro con": additive["torus"],
    "Crear Toro a":   additive["torus"],
    "Crear Toro hasta":additive["torus"],

    #Cuña aditiva
    "Cuña Aditiva":   additive["wedge"],
    "Cuña":           additive["wedge"],
    "Crear Cuña":     additive["wedge"],
    "Crear Cuña con": additive["wedge"],
    "Crear Cuña a":   additive["wedge"],
    "Crear Cuña hasta":additive["wedge"],

    #Ayuda
    "Ayuda":          ayuda,
}

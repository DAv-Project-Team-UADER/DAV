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

import manage as manage
import ayuda as ayuda

TraduceToEs = {
    # Mover elemento
    "Mover elemento":   manage["movefeature"],
    "Mover":           manage["movefeature"],
    "Mover con":       manage["movefeature"],
    "Mover a":         manage["movefeature"],
    "Mover hasta":     manage["movefeature"],
    "Mover objeto":     manage["movefeature"],
    "Mover objeto con": manage["movefeature"],
    "Mover objeto a":   manage["movefeature"],
    "Mover objeto hasta": manage["movefeature"],

    # Mover operación en el árbol
    "Mover operación en el árbol":   manage["movefeatureintree"],
    "Mover operación":               manage["movefeatureintree"],
    "Mover operación con":           manage["movefeatureintree"],
    "Mover operación a":             manage["movefeatureintree"],
    "Mover operación hasta":         manage["movefeatureintree"],
    "Mover operación en el árbol con": manage["movefeatureintree"],
    "Mover operación en el árbol a": manage["movefeatureintree"],
    "Mover operación en el árbol hasta": manage["movefeatureintree"],

    # Mover la punta
    "Mover la punta":   manage["movetip"],
    "Mover punta":      manage["movetip"],
    "Mover la punta con": manage["movetip"],
    "Mover la punta a": manage["movetip"],
    "Mover la punta hasta": manage["movetip"],
    "Mover punta con":  manage["movetip"],
    "Mover punta a":    manage["movetip"],
    "Mover punta hasta": manage["movetip"],
    "Mover la punta del árbol": manage["movetip"],
    "Mover punta del árbol": manage["movetip"],

    #Configuración
    "Configuración": manage["preferences"],
    "Preferencias": manage["preferences"],
    "Configurar": manage["preferences"],
    "Configurar con": manage["preferences"],
    "Configurar a": manage["preferences"],
    "Configurar hasta": manage["preferences"],
    "ajustes": manage["preferences"],
    "Ajustar": manage["preferences"],
    "Ajustar con": manage["preferences"],
    "Ajustar a": manage["preferences"],
    "Ajustar hasta": manage["preferences"],

    #Generador de ejes
    "Generador de ejes": manage["wizardshaft"],
    "generar ejes": manage["wizardshaft"],
    "Generar ejes": manage["wizardshaft"],
    "Generar ejes con": manage["wizardshaft"],
    "Generar ejes a": manage["wizardshaft"],
    "Generar ejes hasta": manage["wizardshaft"],

    "ayuda":                manage["help"],
    "información":          manage["help"],
    "opciones":             manage["help"]
}

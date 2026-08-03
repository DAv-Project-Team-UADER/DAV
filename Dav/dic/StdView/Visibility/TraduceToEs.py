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

"""Spanish spoken-word mapping for the DAV StdView/Visibility dictionary folder."""

from .Visibility import visibility

TraduceToEs = {
    "ocultar objetos":      visibility["hideobjects"],
    "ocultar":              visibility["hide"],
    "todos los enlaces":   visibility["alllinks"],
    "vinculado":            visibility["linked"],
    "vínculo final":        visibility["linkedfinal"],
    "volver atrás":         visibility["selback"],
    "caja de límites":      visibility["boundingbox"],
    "avanzar selección":    visibility["selforward"],
    "seleccionar visibles": visibility["selectvisible"],
    "mostrar objetos":      visibility["showobjects"],
    "mostrar":              visibility["show"],
    "alternar todo":        visibility["toggleall"],
    "seleccionabilidad":    visibility["selectability"],
    "transparencia":        visibility["transparency"],
    "alternar":             visibility["toggle"],
    "alinear a selección":  visibility["aligntoselection"],

    "ocultar objetos":      visibility["hideobjects"],
    "ocultar todo":         visibility["hideobjects"],
    "ocultar todos":        visibility["hideobjects"],
    "esconder objetos":     visibility["hideobjects"],
    "esconder todo":        visibility["hideobjects"],

    "ocultar":              visibility["hide"],
    "esconder":             visibility["hide"],
    "ocultar seleccion":    visibility["hide"],
    "ocultar selección":    visibility["hide"],
    "esconder seleccion":   visibility["hide"],
    "esconder selección":   visibility["hide"],

    "todos los links":      visibility["alllinks"],
    "todos los enlaces":    visibility["alllinks"],
    "seleccionar todos los links": visibility["alllinks"],
    "seleccionar todos los enlaces": visibility["alllinks"],

    "vinculado":            visibility["linked"],
    "objeto vinculado":     visibility["linked"],
    "enlazado":             visibility["linked"],
    "ir al vinculo":        visibility["linked"],
    "ir al vínculo":        visibility["linked"],

    "vinculo final":        visibility["linkedfinal"],
    "vínculo final":        visibility["linkedfinal"],
    "enlace final":         visibility["linkedfinal"],
    "vinculado final":      visibility["linkedfinal"],

    "atras seleccion":      visibility["selback"],
    "atrás selección":      visibility["selback"],
    "retroceder seleccion":  visibility["selback"],
    "retroceder selección":  visibility["selback"],
    "volver seleccion":     visibility["selback"],
    "volver selección":     visibility["selback"],

    "caja de colision":     visibility["boundingbox"],
    "caja de colisión":     visibility["boundingbox"],
    "caja delimitadora":    visibility["boundingbox"],
    "caja limite":          visibility["boundingbox"],
    "caja límite":          visibility["boundingbox"],
    "caja de límites":      visibility["boundingbox"],

    "adelante seleccion":   visibility["selforward"],
    "adelante selección":   visibility["selforward"],
    "avanzar seleccion":    visibility["selforward"],
    "avanzar selección":    visibility["selforward"],

    "seleccionar visibles": visibility["selectvisible"],
    "seleccionar visible":  visibility["selectvisible"],
    "seleccionar objetos visibles": visibility["selectvisible"],

    "mostrar objetos":      visibility["showobjects"],
    "mostrar todo":         visibility["showobjects"],
    "mostrar todos":        visibility["showobjects"],
    "hacer visible todo":   visibility["showobjects"],
    "revelar objetos":      visibility["showobjects"],

    "mostrar":              visibility["show"],
    "revelar":              visibility["show"],
    "mostrar seleccion":    visibility["show"],
    "mostrar selección":    visibility["show"],

    "alternar todo":        visibility["toggleall"],
    "conmutar todo":        visibility["toggleall"],
    "alternar todos":       visibility["toggleall"],

    "seleccionabilidad":    visibility["selectability"],
    "alternar seleccionabilidad": visibility["selectability"],
    "alternar selecciónabilidad": visibility["selectability"],
    "permitir seleccion":   visibility["selectability"],
    "permitir selección":   visibility["selectability"],

    "transparencia":        visibility["transparency"],
    "alternar transparencia": visibility["transparency"],
    "transparente":         visibility["transparency"],

    "alternar":             visibility["toggle"],
    "alternar visibilidad": visibility["toggle"],
    "conmutar visibilidad": visibility["toggle"],

    "alinear a seleccion":  visibility["aligntoselection"],
    "alinear a selección":  visibility["aligntoselection"],
    "alinear con seleccion": visibility["aligntoselection"],
    "alinear con selección": visibility["aligntoselection"],
    "perpendicular a la seleccion": visibility["aligntoselection"],
    "perpendicular a la selección": visibility["aligntoselection"],

    "ayuda":                visibility["help"],
    "información":          visibility["help"],
    "opciones":             visibility["help"],
}
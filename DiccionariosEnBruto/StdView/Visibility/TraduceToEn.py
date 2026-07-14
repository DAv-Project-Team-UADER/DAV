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

"""English spoken-word mapping for the DAV StdView/Visibility dictionary folder."""

from .Visibility import visibility

TraduceToEn = {
    # Main keys
    "hideobjects":      visibility["hideobjects"],
    "hide":             visibility["hide"],
    "alllinks":         visibility["alllinks"],
    "linked":           visibility["linked"],
    "linkedfinal":      visibility["linkedfinal"],
    "selback":          visibility["selback"],
    "boundingbox":      visibility["boundingbox"],
    "selforward":       visibility["selforward"],
    "selectvisible":    visibility["selectvisible"],
    "showobjects":      visibility["showobjects"],
    "show":             visibility["show"],
    "toggleall":        visibility["toggleall"],
    "selectability":    visibility["selectability"],
    "transparency":     visibility["transparency"],
    "toggle":           visibility["toggle"],
    "aligntoselection": visibility["aligntoselection"],

    # Synonyms / Alternative English terms
    "hide objects":     visibility["hideobjects"],
    "hide all":         visibility["hideobjects"],
    "conceal objects":  visibility["hideobjects"],

    "hide selection":   visibility["hide"],
    "hide selected":    visibility["hide"],
    "conceal":          visibility["hide"],

    "all links":        visibility["alllinks"],
    "select all links": visibility["alllinks"],
    "every link":       visibility["alllinks"],

    "linked object":    visibility["linked"],
    "linked target":    visibility["linked"],
    "go to link":       visibility["linked"],

    "linked final":     visibility["linkedfinal"],
    "final link":       visibility["linkedfinal"],
    "deepest link":     visibility["linkedfinal"],

    "selection back":   visibility["selback"],
    "back selection":   visibility["selback"],
    "previous selection": visibility["selback"],
    "go back selection": visibility["selback"],

    "boundary box":     visibility["boundingbox"],
    "bbox":             visibility["boundingbox"],
    "show bounding box": visibility["boundingbox"],

    "selection forward": visibility["selforward"],
    "forward selection": visibility["selforward"],
    "next selection":   visibility["selforward"],
    "go forward selection": visibility["selforward"],

    "select visible":   visibility["selectvisible"],
    "select visible objects": visibility["selectvisible"],
    "select visible only": visibility["selectvisible"],

    "show objects":     visibility["showobjects"],
    "show all":         visibility["showobjects"],
    "reveal objects":   visibility["showobjects"],

    "reveal":           visibility["show"],
    "show selection":   visibility["show"],
    "show selected":    visibility["show"],

    "toggle all":       visibility["toggleall"],
    "toggle everything": visibility["toggleall"],

    "toggle selectability": visibility["selectability"],
    "selectable":       visibility["selectability"],

    "toggle transparency": visibility["transparency"],
    "transparent":      visibility["transparency"],

    "toggle visibility": visibility["toggle"],
    "switch visibility": visibility["toggle"],

    "align to selection": visibility["aligntoselection"],
    "align camera to selection": visibility["aligntoselection"],

    # Help
    "help":             visibility["help"],
    "info":             visibility["help"],
    "options":          visibility["help"],
}
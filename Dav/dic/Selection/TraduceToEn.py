# Copyright (C) 2026 El Equipo del Proyecto DAV
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

from .selection import selection
from .ayuda import ayuda

TraduceToEn = {
    # next
    "advance": selection["next"],
    "forward": selection["next"],
    "skip": selection["next"],
    "next": selection["next"],
    "next object": selection["next"],
    "next item": selection["next"],
    "select next": selection["next"],
    "select next object": selection["next"],
    "object next": selection["next"],

    # previous
    "back": selection["previous"],
    "go back": selection["previous"],
    "previous": selection["previous"],
    "previous object": selection["previous"],
    "previous item": selection["previous"],
    "select previous": selection["previous"],
    "select previous object": selection["previous"],
    "object previous": selection["previous"],

    # selectall
    "all": selection["selectall"],
    "everything": selection["selectall"],
    "select all": selection["selectall"],
    "select all objects": selection["selectall"],
    "select everything": selection["selectall"],

    # deselectall
    "none": selection["deselectall"],
    "nothing": selection["deselectall"],
    "remove": selection["deselectall"],
    "uncheck": selection["deselectall"],
    "uncheck all": selection["deselectall"],
    "deselect": selection["deselectall"],
    "deselect all": selection["deselectall"],
    "clear selection": selection["deselectall"],
    "unselect": selection["deselectall"],
    "clear": selection["deselectall"],

    # current
    "which": selection["current"],
    "this": selection["current"],
    "current": selection["current"],
    "current object": selection["current"],
    "which object": selection["current"],

    # count
    "how many": selection["count"],
    "count": selection["count"],
    "how many objects": selection["count"],

    "help": ayuda,
}

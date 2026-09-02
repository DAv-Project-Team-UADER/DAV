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

TraduceToEs = {
    # next
    "avanzar": selection["next"],
    "otro": selection["next"],
    "otra": selection["next"],
    "pasar": selection["next"],
    "siguiente": selection["next"],
    "siguiente objeto": selection["next"],
    "objeto siguiente": selection["next"],
    "siguiente elemento": selection["next"],
    "seleccionar siguiente": selection["next"],
    "seleccionar siguiente objeto": selection["next"],

    # byname
    "por nombre": selection["byname"],
    "buscar": selection["byname"],
    "buscar objeto": selection["byname"],
    "buscar por nombre": selection["byname"],
    "seleccionar por nombre": selection["byname"],
    "nombre": selection["byname"],
    "llamar": selection["byname"],

    # previous
    "retroceder": selection["previous"],
    "volver": selection["previous"],
    "anterior": selection["previous"],
    "anterior objeto": selection["previous"],
    "objeto anterior": selection["previous"],
    "anterior elemento": selection["previous"],
    "seleccionar anterior": selection["previous"],
    "seleccionar anterior objeto": selection["previous"],

    # selectall
    "todos": selection["selectall"],
    "todo": selection["selectall"],
    "seleccionar todos": selection["selectall"],
    "seleccionar todo": selection["selectall"],
    "seleccionar todos los objetos": selection["selectall"],

    # deselectall
    "nada": selection["deselectall"],
    "ninguno": selection["deselectall"],
    "ninguna": selection["deselectall"],
    "quitar": selection["deselectall"],
    "quitar todos": selection["deselectall"],
    "desmarcar": selection["deselectall"],
    "desmarcar todo": selection["deselectall"],
    "desmarcar todos": selection["deselectall"],
    "deseleccionar": selection["deselectall"],
    "deseleccionar todo": selection["deselectall"],
    "deseleccionar todos": selection["deselectall"],
    "limpiar seleccion": selection["deselectall"],
    "limpiar seleccion": selection["deselectall"],

    # current
    "cual": selection["current"],
    "este": selection["current"],
    "actual": selection["current"],
    "objeto actual": selection["current"],
    "que objeto tengo": selection["current"],

    # count
    "cuantos": selection["count"],
    "cantidad": selection["count"],
    "cuantos objetos": selection["count"],
    "cuantos hay": selection["count"],

    "ayuda": ayuda,
    "help": ayuda,
}

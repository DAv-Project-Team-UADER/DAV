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

TraduceToPt = {
    # next
    "avançar": selection["next"],
    "outro": selection["next"],
    "outra": selection["next"],
    "passar": selection["next"],
    "próximo": selection["next"],
    "próximo objeto": selection["next"],
    "objeto próximo": selection["next"],
    "próximo elemento": selection["next"],
    "selecionar próximo": selection["next"],
    "selecionar próximo objeto": selection["next"],

    # previous
    "voltar": selection["previous"],
    "anterior": selection["previous"],
    "anterior objeto": selection["previous"],
    "objeto anterior": selection["previous"],
    "anterior elemento": selection["previous"],
    "selecionar anterior": selection["previous"],
    "selecionar anterior objeto": selection["previous"],

    # selectall
    "todos": selection["selectall"],
    "tudo": selection["selectall"],
    "selecionar todos": selection["selectall"],
    "selecionar tudo": selection["selectall"],
    "selecionar todos os objetos": selection["selectall"],

    # deselectall
    "nada": selection["deselectall"],
    "nenhum": selection["deselectall"],
    "nenhuma": selection["deselectall"],
    "remover": selection["deselectall"],
    "desmarcar": selection["deselectall"],
    "desmarcar tudo": selection["deselectall"],
    "desmarcar todos": selection["deselectall"],
    "desselecionar": selection["deselectall"],
    "desselecionar tudo": selection["deselectall"],
    "desselecionar todos": selection["deselectall"],
    "limpar seleção": selection["deselectall"],
    "limpar selecao": selection["deselectall"],

    # current
    "qual": selection["current"],
    "este": selection["current"],
    "atual": selection["current"],
    "objeto atual": selection["current"],
    "qual objeto tenho": selection["current"],

    # count
    "quantos": selection["count"],
    "quantidade": selection["count"],
    "quantos objetos": selection["count"],
    "quantos há": selection["count"],

    "ajuda": ayuda,
    "help": ayuda,
}

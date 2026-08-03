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

from .linkActions import link

TraduceToPt = {
    # MakeLink
    "criar link":       link["makelink"],
    "novo link":        link["makelink"],
    "gerar link":       link["makelink"],
    "fazer link":       link["makelink"],

    # RelativeLink
    "link relativo":    link["relativelink"],
    "vincular relativo":link["relativelink"],
    "anexar relativo":  link["relativelink"],
    "referência relativa": link["relativelink"],

    # ImportLink
    "importar link":    link["importlink"],
    "trazer link":      link["importlink"],
    "carregar link":    link["importlink"],
    "adicionar link":   link["importlink"],

    # ImportAllLinks
    "importar todos":   link["importalllinks"],
    "carregar todos":   link["importalllinks"],
    "trazer todos os links": link["importalllinks"],
    "adicionar todos os links": link["importalllinks"],

    # ReplaceLink
    "substituir link":  link["replacelink"],
    "trocar link":      link["replacelink"],
    "alterar link":     link["replacelink"],
    "modificar link":   link["replacelink"],

    # LinkGroups
    "grupo de links":   link["linkgroups"],
    "conjunto de links":link["linkgroups"],
    "coleção de links": link["linkgroups"],
    "agrupamento de links": link["linkgroups"],

    # Help
    "ajuda":            link["help"],
    "informações":      link["help"],
    "opções":           link["help"]
}

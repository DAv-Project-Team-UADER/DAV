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

TraduceToEn = {
    # MakeLink
    "make link":     link["makelink"],
    "create link":  link["makelink"],
    "generate link":link["makelink"],
    "new link":     link["makelink"],

    # RelativeLink
    "relative link":link["relativelink"],
    "linked relative": link["relativelink"],
    "attach relative": link["relativelink"],

    # ImportLink
    "import link":  link["importlink"],
    "bring link":   link["importlink"],
    "load link":    link["importlink"],

    # ImportAllLinks
    "import all":     link["importalllinks"],
    "load all links": link["importalllinks"],
    "bring all links":link["importalllinks"],

    # ReplaceLink
    "replace link": link["replacelink"],
    "substitute link": link["replacelink"],
    "change link":  link["replacelink"],

    # LinkGroups
    "link groups":   link["linkgroups"],
    "group links":  link["linkgroups"],
    "link set":     link["linkgroups"],
    "link cluster": link["linkgroups"],

    # Help
    "help":         link["help"],
    "info":         link["help"],
    "options":      link["help"]
}

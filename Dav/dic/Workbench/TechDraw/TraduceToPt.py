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
# junto me com este programa. Si no es así, consulte <http://www.gnu.org/licenses/>.
# SPDX-License-Identifier: GPL-3.0-or-later

"""Portuguese spoken-word mapping for TechDraw workbench dictionary."""

from .TechDraw import techdraw

TraduceToPt = {
    # Submenús do TechDraw
    "vistas":                 techdraw["views"],
    "vista":                  techdraw["views"],

    "dimensões":              techdraw["dimensions"],
    "dimensoes":              techdraw["dimensions"],
    "cotas":                  techdraw["dimensions"],
    "medidas":                techdraw["dimensions"],

    "linhas":                 techdraw["addlines"],
    "adicionar linhas":       techdraw["addlines"],

    "símbolos":               techdraw["symbols"],
    "simbolos":               techdraw["symbols"],

    "capturas":               techdraw["snaps"],
    "snaps":                  techdraw["snaps"],

    "topologia":              techdraw["topology"],

    "página":                 techdraw["page"],
    "pagina":                 techdraw["page"],
    "folha":                  techdraw["page"],

    "anotações":              techdraw["annotations"],
    "anotacoes":              techdraw["annotations"],
    "notas":                  techdraw["annotations"],

    "hachura":                techdraw["hatching"],
    "hachuras":               techdraw["hatching"],

    "vértices":               techdraw["addvertices"],
    "vertices":               techdraw["addvertices"],

    "outras vistas":          techdraw["otherviews"],

    "recursos":               techdraw["features"],

    "ajuda":                  techdraw["help"],
    "informação":             techdraw["help"],
    "informacao":             techdraw["help"],
}

TraduceToPT = TraduceToPt
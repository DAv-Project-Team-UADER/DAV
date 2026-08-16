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

"""English spoken-word mapping for TechDraw workbench dictionary."""

from .TechDraw import techdraw

TraduceToEn = {
    # TechDraw submenus
    "views":                  techdraw["views"],
    "drawing views":          techdraw["views"],

    "dimensions":             techdraw["dimensions"],
    "dimension":              techdraw["dimensions"],
    "measurements":           techdraw["dimensions"],

    "lines":                  techdraw["addlines"],
    "add lines":              techdraw["addlines"],

    "symbols":                techdraw["symbols"],
    "symbol":                 techdraw["symbols"],

    "snaps":                  techdraw["snaps"],
    "snap":                   techdraw["snaps"],

    "topology":               techdraw["topology"],

    "page":                   techdraw["page"],
    "sheet":                  techdraw["page"],
    "drawing sheet":          techdraw["page"],

    "annotations":            techdraw["annotations"],
    "notes":                  techdraw["annotations"],

    "hatching":               techdraw["hatching"],
    "hatch":                  techdraw["hatching"],

    "vertices":               techdraw["addvertices"],
    "add vertices":           techdraw["addvertices"],

    "other views":            techdraw["otherviews"],
    "auxiliary views":        techdraw["otherviews"],

    "features":               techdraw["features"],

    "help":                   techdraw["help"],
    "info":                   techdraw["help"],
}
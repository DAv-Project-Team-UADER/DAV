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

"""English spoken-word mapping for the DAV PartWorkbench dictionary."""

from .PartWorkbench import part
from .ayuda import ayuda

TraduceToEn = {
    "box": part["box"],
    "create box": part["box"],
    "make box": part["box"],

    "circle": part["circle"],
    "create circle": part["circle"],
    "make circle": part["circle"],

    "cone": part["cone"],
    "create cone": part["cone"],
    "primitive cone": part["primitive cone"],

    "cube": part["cube"],
    "create cube": part["cube"],
    "make cube": part["cube"],

    "cylinder": part["cylinder"],
    "create cylinder": part["cylinder"],
    "primitive cylinder": part["primitive cylinder"],

    "ellipse": part["ellipse"],
    "create ellipse": part["ellipse"],
    "make ellipse": part["ellipse"],

    "line": part["line"],
    "create line": part["line"],
    "make line": part["line"],

    "new sketch": part["nuevo sketch"],
    "create sketch": part["crear sketch"],
    "new drawing": part["nuevo boceto"],

    "chamfer": part["chaflan"],
    "bevel": part["biselar"],
    "create chamfer": part["chaflan"],

    "color per face": part["color por cara"],
    "paint face": part["pintar cara"],
    "color face": part["colorear cara"],

    "cross sections": part["cross sections"],
    "create cross sections": part["cross sections"],
    "make cross sections": part["cross sections"],

    "extrude": part["extrude"],
    "create extrude": part["extrude"],
    "extrude object": part["extruir objeto"],

    "fillet": part["fillet"],
    "round edges": part["redondear bordes"],
    "round": part["redondear"],

    "loft": part["loft"],
    "create loft": part["loft"],
    "make loft": part["hacer loft"],
    "join profiles": part["unir perfiles"],

    "make face": part["make face"],
    "create face": part["crear cara"],
    "face": part["cara"],

    "mirror": part["mirror"],
    "reflect": part["reflejar"],
    "create mirror": part["mirror"],

    "offset": part["offset"],
    "create offset": part["offset"],
    "thicken": part["ensanchar"],
    "shrink": part["encoger"],

    "offset 2d": part["offset 2d"],
    "2d offset": part["offset 2d"],
    "outline": part["contorno"],
    "border": part["borde"],

    "projection": part["projection"],
    "project": part["proyectar"],
    "project on surface": part["projection"],
    "project drawing": part["proyectar dibujo"],

    "revolve": part["revolve"],
    "create revolve": part["revolve"],
    "revolution": part["revolucion"],

    "ruled surface": part["ruled surface"],
    "create ruled surface": part["ruled surface"],
    "join curves": part["unir curvas"],

    "scale": part["scale"],
    "resize": part["scale"],
    "enlarge": part["agrandar"],
    "reduce": part["reducir"],

    "section": part["section"],
    "create section": part["section"],
    "section curve": part["section"],
    "intersection": part["section"],

    "sweep": part["sweep"],
    "create sweep": part["sweep"],
    "sweep profile": part["sweep"],
    "sweep along path": part["sweep"],
    "pipe": part["sweep"],

    "help": ayuda,
    "manual": ayuda,
    "support": ayuda,
    "documentation": ayuda,
}

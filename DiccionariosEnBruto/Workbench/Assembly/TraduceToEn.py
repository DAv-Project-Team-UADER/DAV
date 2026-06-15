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

"""English spoken-word mapping for the DAV AssemblyWorkbench dictionary."""
 
from .Assembly import assembly
from .joint.joint import joint
from .ayuda import ayuda
 
TraduceToEn = {
    "new assembly":      assembly["create"],
    "create assembly":   assembly["create"],
    "new part":          assembly["newpart"],
    "insert part":       assembly["newpart"],
    "insert link":       assembly["link"],
    "link part":         assembly["link"],
    "solve":             assembly["solve"],
    "solve assembly":    assembly["solve"],
    "exploded view":     assembly["view"],
    "create view":       assembly["view"],
    "simulation":        assembly["simulation"],
    "create simulation": assembly["simulation"],
    "bill of materials": assembly["bom"],
    "bom":               assembly["bom"],
    "preferences":       assembly["preferences"],
    "settings":          assembly["preferences"],
    "ground":            assembly["grounded"],
    "toggle grounded":   assembly["grounded"],
    "joint":             joint,
    "help":              ayuda,
}
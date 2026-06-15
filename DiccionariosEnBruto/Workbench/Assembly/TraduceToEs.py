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

"""Spanish spoken-word mapping for the DAV AssemblyWorkbench dictionary."""

from .Assembly import assembly
from .joint.joint import joint
from .ayuda import ayuda

TraduceToEs = {
    # Crear ensamblaje
    "nuevo ensamblaje":      assembly["create"],
    "crear ensamblaje":      assembly["create"],
    "ensamblaje nuevo":      assembly["create"],
    "nuevo ensamble":        assembly["create"],
    "crear ensamble":        assembly["create"],
    "ensamble nuevo":        assembly["create"],
    "ensamblaje":            assembly["create"],
    "ensamble":              assembly["create"],

    # Nueva pieza
    "nueva pieza":           assembly["newpart"],
    "crear pieza":           assembly["newpart"],
    "insertar pieza":        assembly["newpart"],
    "pieza nueva":           assembly["newpart"],

    # Vínculo / Enlace
    "insertar vinculo":      assembly["link"],
    "insertar vínculo":      assembly["link"],
    "vincular pieza":        assembly["link"],
    "vincular":              assembly["link"],
    "enlace":                assembly["link"],
    "insertar enlace":       assembly["link"],
    "vinculo":               assembly["link"],
    "vínculo":               assembly["link"],

    # Resolver
    "resolver":              assembly["solve"],
    "resolver ensamblaje":   assembly["solve"],
    "resolver ensamble":     assembly["solve"],
    "calcular ensamblaje":   assembly["solve"],
    "calcular":              assembly["solve"],

    # Vista explosionada
    "vista explosionada":    assembly["view"],
    "vista explotada":       assembly["view"],
    "crear vista explosionada": assembly["view"],
    "crear vista explotada":    assembly["view"],
    "explosionar":           assembly["view"],
    "explotar":              assembly["view"],

    # Simulación
    "simulacion":            assembly["simulation"],
    "simulación":            assembly["simulation"],
    "crear simulacion":      assembly["simulation"],
    "crear simulación":      assembly["simulation"],
    "simular":               assembly["simulation"],

    # Lista de materiales (BOM)
    "lista de materiales":   assembly["bom"],
    "tabla de materiales":   assembly["bom"],
    "bom":                   assembly["bom"],
    "ldm":                   assembly["bom"],

    # Preferencias / Ajustes
    "preferencias":          assembly["preferences"],
    "configuracion":         assembly["preferences"],
    "configuración":         assembly["preferences"],
    "ajustes":               assembly["preferences"],

    # Fijar pieza (Grounded)
    "fijar pieza":           assembly["grounded"],
    "fijar":                 assembly["grounded"],
    "anclar":                assembly["grounded"],
    "alternar fijacion":     assembly["grounded"],
    "alternar fijación":     assembly["grounded"],
    "fijado":                assembly["grounded"],
    "fijo":                  assembly["grounded"],

    # Sub-contexto de uniones (Joints)
    "union":                 joint,
    "unión":                 joint,
    "junta":                 joint,

    # Ayuda
    "ayuda":                 ayuda,
    "help":                  ayuda,
}
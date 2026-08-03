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

from .StructureToolbar import structure

TraduceToPt = {
    # Part
    "peça":        structure["part"],
    "componente":  structure["part"],
    "elemento":    structure["part"],
    "parte":       structure["part"],

    # Group
    "grupo":       structure["newgroup"],
    "novo grupo":  structure["newgroup"],
    "coleção":     structure["newgroup"],
    "pasta":       structure["newgroup"],

    # LinkActions
    "link":        structure["linkactions"],
    "conectar":    structure["linkactions"],
    "associar":    structure["linkactions"],
    "referência":  structure["linkactions"],

    # Help
    "ajuda":       structure["help"],
    "informações": structure["help"],
    "opções":      structure["help"]
}

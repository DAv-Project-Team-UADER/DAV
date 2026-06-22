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

"""Portuguese spoken-word mapping for Part new sketch commands."""

from .new_sketch import new_sketch
from .ayuda import ayuda

TraduceToPt = {
    "esboco": new_sketch["new sketch"],
    "esboço": new_sketch["new sketch"],
    "novo esboco": new_sketch["new sketch"],
    "novo esboço": new_sketch["new sketch"],
    "criar esboco": new_sketch["new sketch"],
    "criar esboço": new_sketch["new sketch"],
    "fazer esboco": new_sketch["new sketch"],
    "fazer esboço": new_sketch["new sketch"],
    "rascunho": new_sketch["new sketch"],
    "novo rascunho": new_sketch["new sketch"],
    "criar rascunho": new_sketch["new sketch"],
    "fazer rascunho": new_sketch["new sketch"],

    "ajuda":             new_sketch["help"],
    "informação":       new_sketch["help"],
    "opções":            new_sketch["help"]


}
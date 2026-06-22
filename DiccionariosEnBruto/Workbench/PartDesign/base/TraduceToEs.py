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

import base as base
import ayuda as ayuda

TraduceToEs = {
    #Body
    "cuerpo":       base["body"],
    "crear cuerpo": base["body"],
    "cuerpo nuevo": base["body"],
    "nuevo cuerpo": base["body"],
    
    #Nuevo croquis
    "nuevo croquis": base["new sketch"],
    "crear croquis": base["new sketch"],
    "croquis nuevo": base["new sketch"],
    "nuevo boceto": base["new sketch"],
    "crear boceto": base["new sketch"],
    "boceto nuevo": base["new sketch"],

    #Clonar
    "clonar":        base["clone"],
    "clonar objeto": base["clone"],
    "clonar forma":  base["clone"],
    "clonar cuerpo": base["clone"],
    "copiar":         base["clone"],
    "copiar objeto":  base["clone"],
    "copiar forma":   base["clone"],
    "copiar cuerpo":  base["clone"],
    "duplicar":  base["clone"],

    #Enlazador de subformas
    "enlazar subforma": base["subshapebinder"],
    "enlazar subformas": base["subshapebinder"],
    "vincular subforma": base["subshapebinder"],
    "vincular subformas": base["subshapebinder"],
    "subforma enlazada": base["subshapebinder"],
    "subformas enlazadas": base["subshapebinder"],
    "subforma vinculada": base["subshapebinder"],
    "subformas vinculadas": base["subshapebinder"],

    "ayuda":                base["help"],
    "información":          base["help"],
    "opciones":             base["help"]

}

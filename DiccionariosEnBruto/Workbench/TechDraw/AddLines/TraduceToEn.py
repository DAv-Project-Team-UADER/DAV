# Copyright (C) 2026 El Equipo del Proyecto DAV
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

from .addLines import addLines
from .ayuda import ayuda

TraduceToEn = {
    # twolines
    "two lines":         addLines["twolines"],
    "two line center":   addLines["twolines"],    # synonym
    "center line":       addLines["twolines"],    # synonym
    # twopoints
    "two points":        addLines["twopoints"],
    "two point center":  addLines["twopoints"],   # synonym
    "point center line": addLines["twopoints"],   # synonym
    # cosmetic
    "cosmetic":          addLines["cosmetic"],
    "cosmetic line":     addLines["cosmetic"],    # synonym
    "construction line": addLines["cosmetic"],    # synonym
    # decorate
    "decorate":          addLines["decorate"],
    "line style":        addLines["decorate"],    # synonym
    "change line":       addLines["decorate"],    # synonym
    # center
    "center":            addLines["center"],
    "face center":       addLines["center"],      # synonym
    "face center line":  addLines["center"],      # synonym
    # help
    "help":              addLines["help"],
    "info":              addLines["help"],   # synonym
    "options":           addLines["help"],   # synonym
}

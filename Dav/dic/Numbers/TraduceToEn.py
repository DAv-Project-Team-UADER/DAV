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

"""English spoken-word mapping for numeric input."""

from .Numbers import Numbers

TraduceToEn = {
    # Digits 0-9
    "zero":       Numbers["zero"],
    "one":        Numbers["one"],
    "two":        Numbers["two"],
    "three":      Numbers["three"],
    "four":       Numbers["four"],
    "five":       Numbers["five"],
    "six":        Numbers["six"],
    "seven":      Numbers["seven"],
    "eight":      Numbers["eight"],
    "nine":       Numbers["nine"],

    # Decimal separators
    "point":      Numbers["point"],
    "comma":      Numbers["comma"],
    "decimal":    Numbers["point"],

    # 10-19
    "ten":        Numbers["compound"],
    "eleven":     Numbers["compound"],
    "twelve":     Numbers["compound"],
    "thirteen":   Numbers["compound"],
    "fourteen":   Numbers["compound"],
    "fifteen":    Numbers["compound"],
    "sixteen":    Numbers["compound"],
    "seventeen":  Numbers["compound"],
    "eighteen":   Numbers["compound"],
    "nineteen":   Numbers["compound"],

    # Tens 20-90, combine with a following unit: "twenty two"
    "twenty":     Numbers["compound"],
    "thirty":     Numbers["compound"],
    "forty":      Numbers["compound"],
    "fifty":      Numbers["compound"],
    "sixty":      Numbers["compound"],
    "seventy":    Numbers["compound"],
    "eighty":     Numbers["compound"],
    "ninety":     Numbers["compound"],
}

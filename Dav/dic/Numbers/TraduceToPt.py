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

"""Portuguese spoken-word mapping for numeric input."""

from .Numbers import Numbers

TraduceToPt = {
    # Dígitos 0-9
    "zero":       Numbers["zero"],
    "um":         Numbers["one"],
    "uma":        Numbers["one"],
    "dois":       Numbers["two"],
    "duas":       Numbers["two"],
    "três":       Numbers["three"],
    "tres":       Numbers["three"],
    "quatro":     Numbers["four"],
    "cinco":      Numbers["five"],
    "seis":       Numbers["six"],
    "sete":       Numbers["seven"],
    "oito":       Numbers["eight"],
    "nove":       Numbers["nine"],

    # Separadores decimais
    "ponto":      Numbers["point"],
    "vírgula":    Numbers["comma"],
    "virgula":    Numbers["comma"],
    "decimal":    Numbers["point"],

    # 10-19
    "dez":        Numbers["compound"],
    "onze":       Numbers["compound"],
    "doze":       Numbers["compound"],
    "treze":      Numbers["compound"],
    "catorze":    Numbers["compound"],
    "quatorze":   Numbers["compound"],
    "quinze":     Numbers["compound"],
    "dezesseis":  Numbers["compound"],
    "dezessete":  Numbers["compound"],
    "dezoito":    Numbers["compound"],
    "dezenove":   Numbers["compound"],

    # Dezenas 20-90, se combinam com uma unidade seguinte: "vinte e um"
    "vinte":      Numbers["compound"],
    "trinta":     Numbers["compound"],
    "quarenta":   Numbers["compound"],
    "cinquenta":  Numbers["compound"],
    "sessenta":   Numbers["compound"],
    "setenta":    Numbers["compound"],
    "oitenta":    Numbers["compound"],
    "noventa":    Numbers["compound"],

    # Conector entre dezena e unidade ("vinte e um")
    "e":          Numbers["compound"],

    # Sinal negativo (para ângulos de hipérbole/parábola)
    "menos":      Numbers["negative"],
    "negativo":   Numbers["negative"],
}

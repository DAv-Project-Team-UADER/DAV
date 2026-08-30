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

"""Spanish spoken-word mapping for numeric input."""

from .Numbers import Numbers

TraduceToEs = {
    # Dígitos 0-9
    "cero":       Numbers["zero"],
    "uno":        Numbers["one"],
    "un":         Numbers["one"],
    "una":        Numbers["one"],
    "dos":        Numbers["two"],
    "tres":       Numbers["three"],
    "cuatro":     Numbers["four"],
    "cinco":      Numbers["five"],
    "seis":       Numbers["six"],
    "siete":      Numbers["seven"],
    "ocho":       Numbers["eight"],
    "nueve":      Numbers["nine"],

    # Separadores decimales
    "punto":      Numbers["point"],
    "coma":       Numbers["comma"],
    "decimal":    Numbers["point"],

    # 10-19
    "diez":         Numbers["compound"],
    "once":         Numbers["compound"],
    "doce":         Numbers["compound"],
    "trece":        Numbers["compound"],
    "catorce":      Numbers["compound"],
    "quince":       Numbers["compound"],
    "dieciseis":    Numbers["compound"],
    "diecisiete":   Numbers["compound"],
    "dieciocho":    Numbers["compound"],
    "diecinueve":   Numbers["compound"],

    # 20-29 (veinte suelto y las contracciones veintiuno..veintinueve)
    "veinte":       Numbers["compound"],
    "veintiuno":    Numbers["compound"],
    "veintidos":    Numbers["compound"],
    "veintitres":   Numbers["compound"],
    "veinticuatro": Numbers["compound"],
    "veinticinco":  Numbers["compound"],
    "veintiseis":   Numbers["compound"],
    "veintisiete":  Numbers["compound"],
    "veintiocho":   Numbers["compound"],
    "veintinueve":  Numbers["compound"],

    # Decenas 30-90, se combinan con una unidad siguiente: "treinta y dos"
    "treinta":      Numbers["compound"],
    "cuarenta":     Numbers["compound"],
    "cincuenta":    Numbers["compound"],
    "sesenta":      Numbers["compound"],
    "setenta":      Numbers["compound"],
    "ochenta":      Numbers["compound"],
    "noventa":      Numbers["compound"],

    # Conector entre decena y unidad ("treinta y dos")
    "y":            Numbers["compound"],
}

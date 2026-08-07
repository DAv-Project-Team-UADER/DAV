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

# ============================================================
# Traducciones al Español – PartDesign (solo carpetas)
# ============================================================

from .partdesign import partdesign

TraduceToEs = {

    # Carpetas principales
    "base": partdesign["base"],

    # Sinónimos
    "basico": partdesign["base"],
    "fundamental": partdesign["base"],
    "elemental": partdesign["base"],
    "cimiento": partdesign["base"],

    "agregar": partdesign["additive"],
    "añadir": partdesign["additive"],
    "adiciones": partdesign["additive"],
    "sumar": partdesign["additive"],
    "aditivo": partdesign["additive"],

    "restar": partdesign["subtractive"],
    "remover": partdesign["subtractive"],
    "cortar": partdesign["subtractive"],
    "sustractivo": partdesign["subtractive"],
    "eliminar": partdesign["subtractive"],
    "quitar": partdesign["subtractive"],
    "sacar": partdesign["subtractive"],

    "editar": partdesign["modify"],
    "edicion": partdesign["modify"],
    "modificadores": partdesign["modify"],
    "modificar": partdesign["modify"],

    "transformaciones": partdesign["transform"],
    "patrones": partdesign["transform"],
    "transformar": partdesign["transform"],
    "cambiar": partdesign["transform"],
    "convertir": partdesign["transform"],

    "administrar": partdesign["manage"],
    "administracion": partdesign["manage"],
    "configuracion": partdesign["manage"],
    "gestionar": partdesign["manage"],
    "controlar": partdesign["manage"],
    "manejar": partdesign["manage"],
    "organizar": partdesign["manage"],
    "coordinar": partdesign["manage"],

    "ayuda":                partdesign["help"],
    "información":          partdesign["help"],
    "opciones":             partdesign["help"]
}

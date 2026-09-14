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
# English translations – PartDesign (folders only)
# ============================================================

from .partdesign import partdesign
from measure import CreateDimension

TraduceToEn = {

    # Main groups (conceptual folders)
    "base": partdesign["base"],
    "additive": partdesign["additive"],
    "subtractive": partdesign["subtractive"],
    "modify": partdesign["modify"],
    "transform": partdesign["transform"],
    "manage": partdesign["manage"],

    # Synonyms → same folders
    "basic": partdesign["base"],
    "fundamental": partdesign["base"],

    "add": partdesign["additive"],
    "adding": partdesign["additive"],
    "additions": partdesign["additive"],

    "subtract": partdesign["subtractive"],
    "remove": partdesign["subtractive"],
    "cut": partdesign["subtractive"],

    "edit": partdesign["modify"],
    "editing": partdesign["modify"],
    "modifiers": partdesign["modify"],

    "transformations": partdesign["transform"],
    "patterns": partdesign["transform"],

    "management": partdesign["manage"],
    "administration": partdesign["manage"],
    "settings": partdesign["manage"],
    
    "help":            partdesign['help'],
    "info":            partdesign['help'],
    "options":         partdesign['help']
,
    # MEASURE
    "measure": CreateDimension,
    "measure distance": CreateDimension,
    "distance": CreateDimension,
    "dimension": CreateDimension,
    "dimensioning": CreateDimension,
    "meter": CreateDimension,
    "milimeter": CreateDimension,
    "millimeter": CreateDimension,
    "centimeter": CreateDimension,
    "tape measure": CreateDimension,
    "tape tool": CreateDimension,
    "tape": CreateDimension,
    "ruler": CreateDimension,
}
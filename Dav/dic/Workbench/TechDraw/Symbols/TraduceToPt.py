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

from .Symbols import symbols
from .ayuda import ayuda

TraduceToPt = {

    # Símbolo de solda
    "símbolo de solda": symbols["weldsymbol"],
    "simbolo de solda": symbols["weldsymbol"],
    "solda": symbols["weldsymbol"],
    "adicionar solda": symbols["weldsymbol"],

    # Texto enriquecido
    "texto enriquecido": symbols["richtext"],
    "texto": symbols["richtext"],
    "anotação": symbols["richtext"],
    "anotação de texto": symbols["richtext"],

    # Símbolos de acabamento superficial
    "acabamento superficial": symbols["finish"],
    "acabamento": symbols["finish"],
    "símbolo de acabamento": symbols["finish"],
    "simbolo de acabamento": symbols["finish"],

    # Ajuda
    "ajuda": symbols["help"],
    "informação": symbols["help"],
    "opções": symbols["help"],
}

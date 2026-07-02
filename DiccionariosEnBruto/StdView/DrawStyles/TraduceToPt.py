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
# Portuguese translations – StdViews DrawStyles
# ============================================================

from .drawstyles import drawstyles

TraduceToPt = {
    # Estilos principais
    "asis": drawstyles["styleasis"],
    "plano": drawstyles["flatlines"],
    "linha oculta": drawstyles["hiddenline"],
    "sem sombreamento": drawstyles["noshading"],
    "pontos": drawstyles["points"],
    "sombreado": drawstyles["shaded"],
    "arame": drawstyles["wireframe"],

    # Sinônimos
    "como esta": drawstyles["styleasis"],
    "original": drawstyles["styleasis"],

    "linhas planas": drawstyles["flatlines"],
    "plano linhas": drawstyles["flatlines"],

    "oculto": drawstyles["hiddenline"],
    "linhas ocultas": drawstyles["hiddenline"],

    "sem cor": drawstyles["noshading"],
    "sem preenchimento": drawstyles["noshading"],

    "modo pontos": drawstyles["points"],
    "pontilhado": drawstyles["points"],

    "vista sombreada": drawstyles["shaded"],
    "solido": drawstyles["shaded"],

    "wireframe": drawstyles["wireframe"],
    "estrutura": drawstyles["wireframe"],

    "ajuda": drawstyles["help"],
    "informação": drawstyles["help"],
    "opções": drawstyles["help"],
}

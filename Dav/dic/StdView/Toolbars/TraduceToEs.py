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

from .Toolbars import toolbars
from .Toolbars import toolbars as Toolbars
from .ayuda import ayuda

TraduceToEs = {

    # Portapapeles
    "portapapeles": toolbars["clipboard"],
    "copiar": toolbars["clipboard"],
    "pegar": toolbars["clipboard"],
    "cortar": toolbars["clipboard"],

    # Editar
    "editar": toolbars["edit"],
    "edición": toolbars["edit"],
    "edicion": toolbars["edit"],

    # Archivo
    "archivo": toolbars["file"],

    # Barra de ayuda
    "barra de ayuda": toolbars["toolbarshelp"],
    "ayuda de barra": toolbars["toolbarshelp"],
    
    # Vistas
    "vistas": toolbars["views"],
    "vistas individuales": toolbars["views"],
    "barra de vistas": toolbars["views"],

    # Bloquear barras
    "bloquear": toolbars["lock"],
    "bloquear barras": toolbars["lock"],
    "desbloquear barras": toolbars["lock"],

    # Macro
    "macro": toolbars["macro"],
    "macros": toolbars["macro"],

    # Estructura
    "estructura": toolbars["structure"],

    # Vista
    "vista": toolbars["view"],

    # Banco de trabajo
    "banco de trabajo": toolbars["workbench"],
    "workbench": toolbars["workbench"],

    # Ayuda
    "ayuda": Toolbars["help"],
    "información": Toolbars["help"],
    "opciones": Toolbars["help"],
}

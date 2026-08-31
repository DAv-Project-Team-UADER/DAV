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

TraduceToEn = {

    # Clipboard
    "clipboard": toolbars["clipboard"],
    "copy": toolbars["clipboard"],
    "paste": toolbars["clipboard"],
    "cut": toolbars["clipboard"],

    # Edit
    "edit": toolbars["edit"],
    "editing": toolbars["edit"],

    # File
    "file": toolbars["file"],

    # Help toolbar
    "help toolbar": toolbars["toolbarshelp"],
    "toolbar help": toolbars["toolbarshelp"],

    # Individual views
    "views": toolbars["views"],
    "individual views": toolbars["views"],
    "view toolbar": toolbars["views"],

    # Lock toolbars
    "lock": toolbars["lock"],
    "lock toolbars": toolbars["lock"],
    "unlock toolbars": toolbars["lock"],

    # Macro
    "macro": toolbars["macro"],
    "macros": toolbars["macro"],

    # Structure
    "structure": toolbars["structure"],

    # View
    "view": toolbars["view"],

    # Workbench
    "workbench": toolbars["workbench"],

    # Help
    "help": Toolbars["help"],
    "info": Toolbars["help"],
    "options": Toolbars["help"],
}

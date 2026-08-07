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

TraduceToPt = {

    # Área de transferência
    "área de transferência": toolbars["clipboard"],
    "area de transferencia": toolbars["clipboard"],
    "parte de transferência": toolbars["clipboard"],
    "a transferir": toolbars["clipboard"],
    "transferir": toolbars["clipboard"],
    "barra da área de transferência": toolbars["clipboard"],
    "ferramentas": toolbars["clipboard"],
    "copiar": toolbars["clipboard"],
    "colar": toolbars["clipboard"],
    "recortar": toolbars["clipboard"],
    "desfazer": toolbars["clipboard"],
    "refazer": toolbars["clipboard"],

    # Editar
    "editar": toolbars["edit"],
    "edição": toolbars["edit"],
    "edicao": toolbars["edit"],
    "barra de edição": toolbars["edit"],
    "barra de edicao": toolbars["edit"],

    # Arquivo
    "arquivo": toolbars["file"],
    "folha": toolbars["file"],
    "barra de arquivo": toolbars["file"],
    "barra de arquivos": toolbars["file"],

    # Barra de ajuda
    "barra de ajuda": toolbars["toolbarshelp"],
    "ajuda da barra": toolbars["toolbarshelp"],

    # Vistas
    "vistas": toolbars["views"],
    "vistas individuais": toolbars["views"],
    "perspectivas bidimensionais": toolbars["views"],
    "perspectiva da planta": toolbars["views"],
    "planta": toolbars["views"],
    "perspectiva lateral": toolbars["views"],
    "lateral": toolbars["views"],
    "perspectiva frontal": toolbars["views"],
    "frontal": toolbars["views"],
    "barra de vistas": toolbars["views"],

    # Bloquear barras
    "bloquear": toolbars["lock"],
    "bloquear barra": toolbars["lock"],
    "bloquear barras": toolbars["lock"],
    "desbloquear barra": toolbars["lock"],
    "desbloquear barras": toolbars["lock"],

    # Macro
    "macro": toolbars["macro"],
    "macros": toolbars["macro"],
    "barra de macros": toolbars["macro"],
    "criar macro": toolbars["macro"],
    "gravar macro": toolbars["macro"],

    # Estrutura
    "estrutura": toolbars["structure"],
    "barra de estrutura": toolbars["structure"],
    "organização": toolbars["structure"],
    
    # Vista
    "vista": toolbars["view"],
    "barra de vista": toolbars["view"],
    "ver": toolbars["view"],
    "visualizar": toolbars["view"],
    "visualização": toolbars["view"],

    # Bancada
    "bancada": toolbars["workbench"],
    "barra da bancada": toolbars["workbench"],
    "workbench": toolbars["workbench"],
    "bancadas": toolbars["workbench"],
    "iniciar bancada": toolbars["workbench"],
    "iniciar workbench": toolbars["workbench"],
    
    # Ajuda
    "ajuda": Toolbars["help"],
    "informação": Toolbars["help"],
    "opções": Toolbars["help"],
    
}

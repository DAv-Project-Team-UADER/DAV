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

"""Portuguese spoken-word mapping for the DAV base dictionary."""

from Workbench.workbench import workbench as Workbench
from StdView.StdView import StdView
from Explorer.Explorer import explorer
from LineAttributes.LineAttributes import LineAttributes
from integration.launch_preferences import open_preferences

TraduceToPT = {
    # Explorer / arquivos / pastas
    "explorador":    explorer,
    "arquivo":       explorer,
    "arquivos":      explorer,
    "pasta":         explorer,
    "pastas":        explorer,
    "diretório":     explorer,
    "directorio":    explorer,
    "diretorios":    explorer,
    "diretórios":    explorer,

    # Line attributes (atributos de linha)
    "atributos de linha": LineAttributes,
    "diálogo atributos de linha": LineAttributes,
    "dialogo atributos de linha": LineAttributes,
    "janela atributos de linha": LineAttributes,
    "painel atributos de linha": LineAttributes,

    # Std View (visualização padrão)
    "visualización padrão": StdView,
    "visualização padrão": StdView,
    "visualizações padrão": StdView,
    "vista padrão": StdView,
    "vistas padrão": StdView,
    "diálogo visualização padrão": StdView,
    "janela visualização padrão": StdView,

    # Workbench
    "banco de trabalho": Workbench,
    "bancadas de trabalho": Workbench,
    "workbench":       Workbench,
    "workbenches":     Workbench,

    # Preferências
    "preferencias":  open_preferences,
    "configuracoes": open_preferences,
    "ajustes":       open_preferences,
}

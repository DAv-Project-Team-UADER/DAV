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

"""Spanish spoken-word mapping for the DAV base dictionary."""

from Workbench.workbench import workbench as Workbench
from Workbench.Part.Part import part
from Workbench.Part.circle.circle import circle
from StdView.StdView import StdView
from Explorer.Explorer import explorer
from LineAttributes.LineAttributes import LineAttributes
from integration.launch_preferences import open_preferences

TraduceToEs = {
    # Explorer (archivo, edición, ventanas)
    "explorador":    explorer,
    "archivo":       explorer,
    "archivos":      explorer,
    "carpeta":       explorer,
    "carpetas":      explorer,
    "directorio":    explorer,
    "directorios":   explorer,
    "mesa de trabajo": Workbench,
    "banco de trabajo": Workbench,
    "workbench":   Workbench,
    "pieza":       part,
    "part":        part,
    "circulo":     circle["circle"],
    "círculo":     circle["circle"],

    # Line attributes (atributos de linea)
    "atributos de línea": LineAttributes,
    "atributos de linea": LineAttributes,
    "diálogo atributos de línea": LineAttributes,
    "dialogo atributos de linea": LineAttributes,
    "ventana atributos de línea": LineAttributes,
    "panel atributos de línea": LineAttributes,

    # Std View (vista estandar)
    "vista estándar": StdView,
    "vista estandar":  StdView,
    "vistas estándar": StdView,
    "vistas estandar":  StdView,
    "diálogo vista estándar": StdView,
    "ventana vista estándar": StdView,

    # Workbench
    "banco de trabajo": Workbench,
    "bancos de trabajo": Workbench,
    "entorno de trabajo": Workbench,

    # Preferencias
    "preferencias":  open_preferences,
    "configuracion": open_preferences,
    "ajustes":       open_preferences,
}

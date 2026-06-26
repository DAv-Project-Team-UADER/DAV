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

"""English spoken-word mapping for the StdViews Panels dictionary."""

from .panels import Panels
from .ayuda import ayuda

TraduceToEn = {
    # Help command
    "help": ayuda,
    "info": ayuda,
    
    # Panel & Dock views
    "panel": Panels['panel'],
    "panel view": Panels['panel'],
    "dock": Panels['dock'],
    "dock view": Panels['dock'],
    "undock": Panels['undock'],
    "undock view": Panels['undock'],
    
    # Fullscreen
    "fullscreen": Panels['fullscreen'],
    "full screen": Panels['fullscreen'],
    "toggle fullscreen": Panels['fullscreen'],
    
    # Specific FreeCAD Views
    "dag view": Panels['dagview'],
    "combo view": Panels['comboview'],
    "selection view": Panels['selectionview'],
    "task view": Panels['tasks'],
    "tasks": Panels['tasks'],
    "property view": Panels['properties'],
    "properties": Panels['properties'],
    "tree view": Panels['treeview'],
    
    # Consoles & Bars
    "python console": Panels['console'],
    "console": Panels['console'],
    "report view": Panels['report'],
    "report": Panels['report'],
    "status bar": Panels['statusbar']
}
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

"""Spanish spoken-word mapping for the StdViews Panels dictionary."""

from .panels import Panels
from .ayuda import ayuda

TraduceToEs = {
    # Comando de ayuda
    "ayuda": ayuda,
    "info": ayuda,
    
    # Vistas de Panel y Acoplamiento
    "panel": Panels['panel'],
    "vista de panel": Panels['panel'],
    "acoplar": Panels['dock'],
    "vista acoplada": Panels['dock'],
    "desacoplar": Panels['undock'],
    "vista desacoplada": Panels['undock'],
    
    # Pantalla completa
    "pantalla completa": Panels['fullscreen'],
    "ver pantalla completa": Panels['fullscreen'],
    
    # Paneles específicos de FreeCAD
    "vista dag": Panels['dagview'],
    "vista combo": Panels['comboview'],
    "panel combo": Panels['comboview'],
    "vista de seleccion": Panels['selectionview'],
    "panel de seleccion": Panels['selectionview'],
    "vista de tareas": Panels['tasks'],
    "tareas": Panels['tasks'],
    "panel de tareas": Panels['tasks'],
    "vista de propiedades": Panels['properties'],
    "propiedades": Panels['properties'],
    "panel de propiedades": Panels['properties'],
    "vista de arbol": Panels['treeview'],
    "arbol del modelo": Panels['treeview'],
    
    # Consolas y Barras
    "consola python": Panels['console'],
    "consola": Panels['console'],
    "vista de reporte": Panels['report'],
    "reporte": Panels['report'],
    "barra de estado": Panels['statusbar']
}
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

"""English spoken-word mapping for the Sketcher tools dictionary."""

from .tools import tools
from .ayuda import ayuda
from measure import CreateDimension

TraduceToEn = {
    
    # Delete constraints & synonyms
    "deleteconstraints": tools['deleteconstraints'],
    "delete constraints": tools['deleteconstraints'],
    "clear constraints": tools['deleteconstraints'],
    "remove constraints": tools['deleteconstraints'],
    
    # Delete geometry & synonyms
    "deletegeometry": tools['deletegeometry'],
    "delete geometry": tools['deletegeometry'],
    "clear geometry": tools['deletegeometry'],
    "clear sketch": tools['deletegeometry'],
    "erase sketch": tools['deletegeometry'],
    
    # Merge & synonyms
    "merge": tools['merge'],
    "merge sketches": tools['merge'],
    "combine sketches": tools['merge'],
    
    # Reorient & synonyms
    "reorient": tools['reorient'],
    "reorient sketch": tools['reorient'],
    "change sketch plane": tools['reorient'],
    
    # Remove axes alignment & synonyms
    "removeaxes": tools['removeaxes'],
    "remove axes": tools['removeaxes'],
    "clear axes alignment": tools['removeaxes'],

    "help": tools['help'],
    "info": tools['help'],
    "options": tools['help']
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
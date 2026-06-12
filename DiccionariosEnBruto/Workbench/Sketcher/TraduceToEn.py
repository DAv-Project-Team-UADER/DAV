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

"""English spoken-word mapping for the Sketcher workbench."""

import FreeCADGui as Gui

# Importaciones relativas porque estamos en la misma carpeta
from .sketcher import _toggle_construction
from .ayuda import ayuda as sketcher_ayuda
from .sketcher import sketcher

TraduceToEn = {

    # Carpetas de Sketcher
    "geometry": sketcher["geometry"],
    "geometric": sketcher["geometry"],

    "arcslot": sketcher["arcslot"],
    "arcs": sketcher["arcslot"],
    "arc": sketcher["arcslot"],
    
    "constraints": sketcher["constraints"],
    "constraint": sketcher["constraints"],
    "restrictions": sketcher["constraints"],
    
    "external": sketcher["external"],
    
    "oblong": sketcher["oblong"],
    "create oblong": sketcher["oblong"],
    
    "point": sketcher["point"],
    "create point": sketcher["point"],
    
    "select": sketcher["select"],
    "selection": sketcher["select"],
    
    "slot": sketcher["slot"],
    "create slot": sketcher["slot"],
    
    "square": sketcher["square"],
    "create square": sketcher["square"],
    "draw square": sketcher["square"],
    
    "text": sketcher["text"],
    "write text": sketcher["text"],
    "create text": sketcher["text"],
    
    "tools": sketcher["tools"],
    "tool": sketcher["tools"],
    
    "triangle": sketcher["triangle"],
    "create triangle": sketcher["triangle"],
    "draw triangle": sketcher["triangle"],
    
    "validate": sketcher["validate"],
    "validate sketch": sketcher["validate"],
    
    "view": sketcher["view"],
    "view sketch": sketcher["view"],
    "view selection": sketcher["view"],
    
    # --- Traducciones de la parte inferior de sketcher.py ---
    
    # Control del Boceto / Sketch
    "new": lambda: Gui.runCommand('Sketcher_NewSketch', 0),
    "new sketch": lambda: Gui.runCommand('Sketcher_NewSketch', 0),
    "create sketch": lambda: Gui.runCommand('Sketcher_NewSketch', 0),

    "edit": lambda: Gui.runCommand('Sketcher_EditSketch', 0),
    "edit sketch": lambda: Gui.runCommand('Sketcher_EditSketch', 0),
    "modify sketch": lambda: Gui.runCommand('Sketcher_EditSketch', 0),

    "attach": lambda: Gui.runCommand('Sketcher_MapSketch', 0),
    "map sketch": lambda: Gui.runCommand('Sketcher_MapSketch', 0),
    "attach sketch": lambda: Gui.runCommand('Sketcher_MapSketch', 0),

    "grid": lambda: Gui.runCommand('Sketcher_Grid', 0),
    "toggle grid": lambda: Gui.runCommand('Sketcher_Grid', 0),
    "show grid": lambda: Gui.runCommand('Sketcher_Grid', 0),

    "stop": lambda: Gui.runCommand('Sketcher_StopOperation', 0),
    "stop operation": lambda: Gui.runCommand('Sketcher_StopOperation', 0),
    "abort": lambda: Gui.runCommand('Sketcher_StopOperation', 0),

    "leave": lambda: Gui.runCommand('Sketcher_LeaveSketch', 0),
    "leave sketch": lambda: Gui.runCommand('Sketcher_LeaveSketch', 0),
    "exit sketch": lambda: Gui.runCommand('Sketcher_LeaveSketch', 0),
    "close sketch": lambda: Gui.runCommand('Sketcher_LeaveSketch', 0),

    "cancelediting": lambda: Gui.runCommand('Sketcher_StopEditing', 0),
    "cancel editing": lambda: Gui.runCommand('Sketcher_StopEditing', 0),
    "stop editing": lambda: Gui.runCommand('Sketcher_StopEditing', 0),

    # Geometría de Construcción
    "toggleconstruction": _toggle_construction,
    "toggle construction": _toggle_construction,
    "construction mode": _toggle_construction,

    # Edición y Portapapeles
    "carboncopy": lambda: Gui.runCommand('Sketcher_CarbonCopy', 0),
    "carbon copy": lambda: Gui.runCommand('Sketcher_CarbonCopy', 0),

    "copyelements": lambda: Gui.runCommand('Sketcher_CopyClipboard', 0),
    "copy elements": lambda: Gui.runCommand('Sketcher_CopyClipboard', 0),
    "copy geometry": lambda: Gui.runCommand('Sketcher_CopyClipboard', 0),

    "cutelements": lambda: Gui.runCommand('Sketcher_Cut', 0),
    "cut elements": lambda: Gui.runCommand('Sketcher_Cut', 0),
    "cut geometry": lambda: Gui.runCommand('Sketcher_Cut', 0),

    "pasteelements": lambda: Gui.runCommand('Sketcher_Paste', 0),
    "paste elements": lambda: Gui.runCommand('Sketcher_Paste', 0),
    "paste geometry": lambda: Gui.runCommand('Sketcher_Paste', 0),

    # Transformaciones y Modificaciones
    "mirror": lambda: Gui.runCommand('Sketcher_Symmetry', 0),
    "symmetry": lambda: Gui.runCommand('Sketcher_Symmetry', 0),
    "mirror elements": lambda: Gui.runCommand('Sketcher_Symmetry', 0),

    "mirrorsketch": lambda: Gui.runCommand('Sketcher_MirrorSketch', 0),
    "mirror sketch": lambda: Gui.runCommand('Sketcher_MirrorSketch', 0),

    "offset": lambda: Gui.runCommand('Sketcher_Offset', 0),
    "create offset": lambda: Gui.runCommand('Sketcher_Offset', 0),

    "movearray": lambda: Gui.runCommand('Sketcher_Translate', 0),
    "translate": lambda: Gui.runCommand('Sketcher_Translate', 0),
    "move elements": lambda: Gui.runCommand('Sketcher_Translate', 0),

    "rotatepolar": lambda: Gui.runCommand('Sketcher_Rotate', 0),
    "rotate": lambda: Gui.runCommand('Sketcher_Rotate', 0),
    "rotate elements": lambda: Gui.runCommand('Sketcher_Rotate', 0),

    "scale": lambda: Gui.runCommand('Sketcher_Scale', 0),
    "scale elements": lambda: Gui.runCommand('Sketcher_Scale', 0),

    # Operaciones de Bordes / Esquinas
    "trimedge": lambda: Gui.runCommand('Sketcher_Trimming', 0),
    "trim": lambda: Gui.runCommand('Sketcher_Trimming', 0),
    "trim edge": lambda: Gui.runCommand('Sketcher_Trimming', 0),

    "splitedge": lambda: Gui.runCommand('Sketcher_Split', 0),
    "split": lambda: Gui.runCommand('Sketcher_Split', 0),
    "split edge": lambda: Gui.runCommand('Sketcher_Split', 0),

    "extendedge": lambda: Gui.runCommand('Sketcher_Extend', 0),
    "extend": lambda: Gui.runCommand('Sketcher_Extend', 0),
    "extend edge": lambda: Gui.runCommand('Sketcher_Extend', 0),

    "fillet": lambda: Gui.runCommand('Sketcher_CreateFillet', 0),
    "create fillet": lambda: Gui.runCommand('Sketcher_CreateFillet', 0),

    "chamfer": lambda: Gui.runCommand('Sketcher_CreateChamfer', 0),
    "create chamfer": lambda: Gui.runCommand('Sketcher_CreateChamfer', 0),

    # Soporte y Ayuda
    "help": sketcher_ayuda,
    "get help": sketcher_ayuda,
    "show help": sketcher_ayuda,
}

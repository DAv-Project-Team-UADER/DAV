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

import FreeCADGui as Gui

from .ayuda import ayuda

# Diccionario DAV - StdView / DrawStyles
drawstyles = {
   'styleasis':  lambda: Gui.runCommand('Std_DrawStyle', 0),
   'points':     lambda: Gui.runCommand('Std_DrawStyle', 1),
   'wireframe':  lambda: Gui.runCommand('Std_DrawStyle', 2),
   'hiddenline': lambda: Gui.runCommand('Std_DrawStyle', 3),
   'noshading':  lambda: Gui.runCommand('Std_DrawStyle', 4),
   'shaded':     lambda: Gui.runCommand('Std_DrawStyle', 5),
   'flatlines':  lambda: Gui.runCommand('Std_DrawStyle', 6),
   'help':       ayuda,
}

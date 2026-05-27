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

# Diccionario DAV - StdView / DrawStyles
drawstyles = {
    'styleasis': lambda: Gui.runCommand('Std_DrawStyleAsIs', 0),
    'flatlines': lambda: Gui.runCommand('Std_DrawStyleFlatLines', 0),
    'hiddenline': lambda: Gui.runCommand('Std_DrawStyleHiddenLine', 0),
    'noshading': lambda: Gui.runCommand('Std_DrawStyleNoShading', 0),
    'points': lambda: Gui.runCommand('Std_DrawStylePoints', 0),
    'shaded': lambda: Gui.runCommand('Std_DrawStyleShaded', 0),
    'wireframe': lambda: Gui.runCommand('Std_DrawStyleWireframe', 0),
}

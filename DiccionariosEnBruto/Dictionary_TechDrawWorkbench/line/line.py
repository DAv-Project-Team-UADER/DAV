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

# Diccionario del subgrupo Line (Geometría auxiliar, líneas cosméticas y símbolos)
line = {
    'cosmetic': lambda: Gui.runCommand('TechDraw_2PointCosmeticLine', 0),
    'leader': lambda: Gui.runCommand('TechDraw_LeaderLine', 0),
    'midpoints': lambda: Gui.runCommand('TechDraw_Midpoints', 0),
    'quadrants': lambda: Gui.runCommand('TechDraw_Quadrants', 0),
    'surface': lambda: Gui.runCommand('TechDraw_SurfaceFinishSymbols', 0),
    'help': ayuda
}